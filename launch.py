from modules import launch_utils

args = launch_utils.args
python = launch_utils.python
git = launch_utils.git
index_url = launch_utils.index_url
dir_repos = launch_utils.dir_repos

commit_hash = launch_utils.commit_hash
git_tag = launch_utils.git_tag

run = launch_utils.run
is_installed = launch_utils.is_installed
repo_dir = launch_utils.repo_dir

run_pip = launch_utils.run_pip
check_run_python = launch_utils.check_run_python
git_clone = launch_utils.git_clone
git_pull_recursive = launch_utils.git_pull_recursive
list_extensions = launch_utils.list_extensions
run_extension_installer = launch_utils.run_extension_installer
prepare_environment = launch_utils.prepare_environment
configure_for_tests = launch_utils.configure_for_tests
start = launch_utils.start

parser = argparse.ArgumentParser(
    prog="SillyTavern Extras", description="Web API for transformers models"
)
parser.add_argument(
    "--port", type=int, help="Specify the port on which the application is hosted"
)
parser.add_argument(
    "--listen", action="store_true", help="Host the app on the local network"
)
parser.add_argument(
    "--share", action="store_true", help="Share the app on CloudFlare tunnel"
)
parser.add_argument("--cpu", action="store_true", help="Run the models on the CPU")
parser.add_argument("--cuda", action="store_false", dest="cpu", help="Run the models on the GPU")
parser.add_argument("--cuda-device", help="Specify the CUDA device to use")
parser.add_argument("--mps", "--apple", "--m1", "--m2", action="store_false", dest="cpu", help="Run the models on Apple Silicon")
parser.set_defaults(cpu=True)
parser.add_argument("--summarization-model", help="Load a custom summarization model")
parser.add_argument(
    "--classification-model", help="Load a custom text classification model"
)
parser.add_argument("--captioning-model", help="Load a custom captioning model")
parser.add_argument("--embedding-model", help="Load a custom text embedding model")
parser.add_argument("--chroma-host", help="Host IP for a remote ChromaDB instance")
parser.add_argument("--chroma-port", help="HTTP port for a remote ChromaDB instance (defaults to 8000)")
parser.add_argument("--chroma-folder", help="Path for chromadb persistence folder", default='.chroma_db')
parser.add_argument('--chroma-persist', help="ChromaDB persistence", default=True, action=argparse.BooleanOptionalAction)
parser.add_argument(
    "--secure", action="store_true", help="Enforces the use of an API key"
)
sd_group = parser.add_mutually_exclusive_group()

local_sd = sd_group.add_argument_group("sd-local")
local_sd.add_argument("--sd-model", help="Load a custom SD image generation model")
local_sd.add_argument("--sd-cpu", help="Force the SD pipeline to run on the CPU", action="store_true")

remote_sd = sd_group.add_argument_group("sd-remote")
remote_sd.add_argument(
    "--sd-remote", action="store_true", help="Use a remote backend for SD"
)
remote_sd.add_argument(
    "--sd-remote-host", type=str, help="Specify the host of the remote SD backend"
)
remote_sd.add_argument(
    "--sd-remote-port", type=int, help="Specify the port of the remote SD backend"
)
remote_sd.add_argument(
    "--sd-remote-ssl", action="store_true", help="Use SSL for the remote SD backend"
)
remote_sd.add_argument(
    "--sd-remote-auth",
    type=str,
    help="Specify the username:password for the remote SD backend (if required)",
)

parser.add_argument(
    "--enable-modules",
    action=SplitArgs,
    default=[],
    help="Override a list of enabled modules",
)

args = parser.parse_args()

port = args.port if args.port else 5100
host = "0.0.0.0" if args.listen else "localhost"
summarization_model = (
    args.summarization_model
    if args.summarization_model
    else DEFAULT_SUMMARIZATION_MODEL
)
classification_model = (
    args.classification_model
    if args.classification_model
    else DEFAULT_CLASSIFICATION_MODEL
)
captioning_model = (
    args.captioning_model if args.captioning_model else DEFAULT_CAPTIONING_MODEL
)
embedding_model = (
    args.embedding_model if args.embedding_model else DEFAULT_EMBEDDING_MODEL
)

sd_use_remote = False if args.sd_model else True
sd_model = args.sd_model if args.sd_model else DEFAULT_SD_MODEL
sd_remote_host = args.sd_remote_host if args.sd_remote_host else DEFAULT_REMOTE_SD_HOST
sd_remote_port = args.sd_remote_port if args.sd_remote_port else DEFAULT_REMOTE_SD_PORT
sd_remote_ssl = args.sd_remote_ssl
sd_remote_auth = args.sd_remote_auth

modules = (
    args.enable_modules if args.enable_modules and len(args.enable_modules) > 0 else []
)

if len(modules) == 0:
    print(
        f"{Fore.RED}{Style.BRIGHT}You did not select any modules to run! Choose them by adding an --enable-modules option"
    )
    print(f"Example: --enable-modules=caption,summarize{Style.RESET_ALL}")

def main():
    launch_utils.startup_timer.record("initial startup")

    with launch_utils.startup_timer.subcategory("prepare environment"):
        if not args.skip_prepare_environment:
            prepare_environment()

    if args.test_server:
        configure_for_tests()

    start()


if __name__ == "__main__":
    main()
