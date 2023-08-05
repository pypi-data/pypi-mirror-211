import logging

main_log = logging.getLogger("E620py")
main_log.setLevel(logging.INFO)

# * debugging vars
consolelog_format = logging.Formatter(
    '%(asctime)s - %(name)s : %(levelname)s - %(message)s', datefmt='%H:%M:%S'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(consolelog_format)
main_log.addHandler(console_handler)
