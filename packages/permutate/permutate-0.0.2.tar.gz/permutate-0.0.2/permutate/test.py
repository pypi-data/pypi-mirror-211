from jinja2 import FileSystemLoader, Environment
from permutate import get_root_directory
template_env = Environment(loader=FileSystemLoader(searchpath=f"{get_root_directory()}/templates"))
template = template_env.get_template("job_result_template.html")

print(template)