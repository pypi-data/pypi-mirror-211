from .main import run
import logging

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Ensure logger logs to console
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

run()
