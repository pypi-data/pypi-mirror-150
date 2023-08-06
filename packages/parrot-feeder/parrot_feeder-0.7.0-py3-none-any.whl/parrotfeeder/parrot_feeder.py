#!/usr/bin/env python3
import io
import os
import tarfile
import zipfile
from pathlib import Path
from threading import Thread

from flask import Flask, flash, request, redirect, render_template, jsonify, send_file, Response
from flask_autoindex import AutoIndex
from pyngrok import ngrok
from werkzeug.utils import secure_filename

from squire import Squire

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 4200
DEFAULT_DIRECTORY = os.getcwd()

TELEGRAM_BOT_TOKEN_PARAMETER_NAME = "TELEGRAM_BOT_TOKEN"
TELEGRAM_WHITELIST_PARAMETER_NAME = "TELEGRAM_BOT_WHITELIST"

def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='The parrot-feeder server')
    parser.add_argument('--debug',
                        dest='debug',
                        required=False,
                        action='store_true',
                        help="Enable debug mode")
    parser.add_argument('-i',
                        "--ip",
                        dest="ip",
                        required=False,
                        default=DEFAULT_IP,
                        type=str,
                        help="The local IP address to bind to. "
                             f"Default is {DEFAULT_IP}.")
    parser.add_argument('-p',
                        "--port",
                        dest="port",
                        required=False,
                        default=DEFAULT_PORT,
                        type=str,
                        help="The local TCP port to bind to. "
                             f"Default is {DEFAULT_PORT}.")
    parser.add_argument('-d',
                        "--directory",
                        dest="directory",
                        required=False,
                        default=DEFAULT_DIRECTORY,
                        type=str,
                        help="The local directory to shave over the ngrok network. "
                             "Default is the current working directory.")
    parser.add_argument('-pf',
                        '--print-files',
                        dest='print_files',
                        action='store_true',
                        required=False,
                        help="Specify if the script should print URLs to files found in the shared directory "
                             "for them to be copy-pasted. "
                             "By default the script doesn't print them.")
    parser.add_argument('--telegram-bot-token',
                        dest='telegram_bot_token',
                        required=False,
                        type=str,
                        help="Specify an access token for the Squire telegram bot. "
                             f"The environment variable {TELEGRAM_BOT_TOKEN_PARAMETER_NAME} always has the priority over this argument.")
    parser.add_argument('--telegram-users-whitelist',
                        dest='telegram_users_whitelist',
                        required=False,
                        type=str,
                        help="Specify a comma-separated list of telegram usernames allowed to use the bot. "
                             "This argument needs to be specified "
                             "if you're enabling the squire bot by giving the --telegram-bot-token argument."
                             f"The environment variable {TELEGRAM_WHITELIST_PARAMETER_NAME} "
                             f"always has the priority over this argument.")
    options = parser.parse_args()
    if os.getenv(TELEGRAM_BOT_TOKEN_PARAMETER_NAME):
        options.telegram_bot_token = os.getenv(TELEGRAM_BOT_TOKEN_PARAMETER_NAME)
    if os.getenv(TELEGRAM_WHITELIST_PARAMETER_NAME):
        options.telegram_users_whitelist = os.getenv(TELEGRAM_WHITELIST_PARAMETER_NAME)
    if options.telegram_bot_token and not options.telegram_users_whitelist:
        parser.error("--telegram-users-whitelist must be specified if you're using --telegram-bot-token")
    if not options.telegram_bot_token and options.telegram_users_whitelist:
        parser.error("--telegram-bot-token must be specified if you're using --telegram-users-whitelist")
    return options


class TunneledHttpServer:
    def __init__(self, ip: str,
                 port: int,
                 directory: str,
                 print_files: bool = False,
                 debug: bool = False):
        self.ip = ip
        self.port = port
        self.directory = directory
        self.print_files = print_files
        self.debug = debug

        self.app = Flask(__name__)
        self.app.config['LAST_USED_DIR'] = None

        def _add_to_archive(add_f: callable, path: Path):
            arcname_offset = len(path.parents)
            if path.is_dir():
                for f_name in path.glob("**/*"):
                    add_f(f_name, Path(*f_name.parts[arcname_offset:]))
            else:
                add_f(path, Path(*path.parts[arcname_offset:]))

        def _make_zip(path):
            path = Path(path)
            data = io.BytesIO()
            with zipfile.ZipFile(data, mode='w') as z:
                _add_to_archive(z.write, path)
            data.seek(0)

            return data, 'application/zip', f'{path.stem}.zip'

        def _make_tar(path):
            path = Path(path)
            data = io.BytesIO()
            with tarfile.TarFile(fileobj=data, mode='w') as tar:
                _add_to_archive(tar.add, path)
            data.seek(0)

            return data, 'application/tar', f'{path.stem}.tar.gz'

        def serve_file(path, ftype):
            if ftype == "zip":
                data, mimetype, fname = _make_zip(path)
            elif ftype == "tar":
                data, mimetype, fname = _make_tar(path)
            else:
                raise ValueError(f"Wrong file type {ftype}")

            return data, mimetype, fname

        def save_file(files, save_dir):
            if 'file' not in request.files:
                raise FileNotFoundError('Select the file to upload')

            file = request.files['file']

            if file.filename == '':
                raise ValueError('Empty filename')

            if not file:
                raise ValueError('Empty file')

            filename = secure_filename(file.filename)

            upload_dir_path = Path(save_dir).absolute()
            upload_dir_path.mkdir(parents=True, exist_ok=True)

            full_file_path = upload_dir_path / filename
            file.save(str(full_file_path))

            self.app.config['LAST_USED_DIR'] = str(upload_dir_path)
            self.app.logger.info(f"Uploaded {full_file_path}")

            return full_file_path

        def dir_info(path):
            path = Path(path).absolute()
            dir_exists = False
            breadcrumbs = []
            content = []

            for i, part in enumerate(path.parts):
                p = Path(*path.parts[:i + 1])
                item = {
                    "name": part,
                    "absolute": str(p.absolute()),
                }
                breadcrumbs.append(item)

            if path.is_dir():
                dir_exists = True
                for c in path.glob("*"):
                    item = {
                        "name": c.name,
                        "absolute": str(c.absolute()),
                        "is_dir": c.is_dir(),
                    }
                    content.append(item)

            response = {
                "exists": dir_exists,
                "breadcrumbs": breadcrumbs,
                "parent": str(path.parent),
                "content": content,
            }

            return response

        @self.app.route('/api/upload', methods=['GET', 'POST'])
        def homepage():
            if request.method == 'POST':
                self.app.logger.info(request.files)
                try:
                    files = request.files
                    save_dir = request.form['path']
                    full_file_path = save_file(files, save_dir)
                    flash(f"{full_file_path} uploaded successfully", 'action-success')
                except (FileNotFoundError, ValueError) as e:
                    flash(str(e), 'action-fail')

                return redirect(request.url)

            return render_template("index.html", last_used_dir=self.app.config['LAST_USED_DIR'])

        @self.app.route('/api/path', methods=["POST"])
        def resolve_path():
            path = request.json

            response = dir_info(path)

            return jsonify(response)

        @self.app.route('/api/download', methods=['GET'])
        def download():
            try:
                path = request.args["path"]
                ftype = request.args["ftype"]

                data, mimetype, fname = serve_file(path, ftype)
                return send_file(
                    data,
                    mimetype=mimetype,
                    as_attachment=True,
                    attachment_filename=fname
                )
            except KeyError as e:
                return Response(str(e), status=404)
            except ValueError as e:
                return Response(str(e), status=404)

        AutoIndex(self.app, browse_root=self.directory)

    def start(self):
        self.app.config.from_mapping(
            BASE_URL=f"http://{self.ip}:{self.port}",
            USE_NGROK=True
        )
        self.public_url = ngrok.connect(self.port, bind_tls=True).public_url
        print(f" * Ngrok tunnel {self.public_url} -> http://{self.ip}:{self.port}/")
        print(f" * Serving files from the '{self.directory}' directory")

        if self.print_files:
            for current_path, folders, files in os.walk(self.directory):
                for file in files:
                    relpath = os.path.relpath(os.path.join(current_path, file))
                    relpath = relpath.replace(f'..{os.linesep}', '').replace(f"{self.directory[1:]}", '')
                    print(f" * Serving '{self.public_url}/{relpath}'")
        else:
            print(f" * Hint: use -pf or --print-files for printing URLs for all the files shared over ngflask")
        self.app.config["BASE_URL"] = self.public_url

        self.flask_thread = Thread(target=self.app.run, args=(self.ip, self.port, self.debug))
        self.flask_thread.start()


def main():
    options = get_arguments()
    tunneled_http_server = TunneledHttpServer(ip=options.ip,
                                              port=options.port,
                                              directory=options.directory,
                                              print_files=options.print_files,
                                              debug=options.debug)
    tunneled_http_server.start()

    telegram_bot_token = options.telegram_bot_token
    if telegram_bot_token:
        users_whitelist = [line.strip() for line in options.telegram_users_whitelist.split(",") if line.strip()]
        print(" * Starting the squire telegram bot")
        print(f" * Access allowed to: {users_whitelist}")
        Squire(token=telegram_bot_token, users_whitelist=users_whitelist)


if __name__ == '__main__':
    main()