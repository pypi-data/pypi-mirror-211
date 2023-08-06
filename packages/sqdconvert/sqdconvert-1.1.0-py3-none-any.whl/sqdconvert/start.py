import os
import argparse

from yaspin import yaspin
from yaspin.spinners import Spinners

from . import __name__ as name
from . import color
from .utils import fs
from .config import Config

__all__ = [
    "main"
]

def main(args: argparse.ArgumentParser, config: Config) -> None:
    if args.interactive:
        args.input = input(f"{color.bright_blue}File to convert: {color.bright_white}").strip()
        args.output = input(f"{color.bright_blue}Convert to: {color.bright_white}").strip()

        if args.input.startswith('"') and args.input.endswith('"'):
            args.input = args.input.lstrip('"').rstrip('"')
        
        if args.output.startswith('"') and args.output.endswith('"'):
            args.output = args.output.lstrip('"').rstrip('"')
    
    if args.input is None or args.output is None:
        print(f"{color.bright_red}💥 Provide atleast one argument! {color.bright_green}Maybe you want to try using '{color.bright_yellow}{name} -i{color.bright_green}'?{color.reset}")
        return print(f"{color.bright_green}❓ Use '{color.bright_yellow}{name} -h{color.bright_green}' for a list of commands.{color.reset}")
    
    with yaspin(Spinners.dots12, text=f"{color.bright_white}Converting your file...{color.reset}", color="blue") as spinner:
        inp = os.path.normpath(args.input)
        if os.path.exists(inp):
            if not os.path.isfile(inp):
                spinner.text = f"{color.red}Input at the specified location is not a file: {color.bright_yellow}'{inp}'{color.reset}"
                spinner.fail(f"💥")
                exit()
        else:
            spinner.text = f"{color.red}File not found: {color.bright_yellow}'{inp}'{color.reset}"
            spinner.fail(f"💥")
            exit()

        out = os.path.normpath(args.output)
        if os.path.exists(out):
            spinner.text = f"{color.red}File already exists: {color.bright_yellow}'{out}'{color.reset}"
            spinner.fail(f"💥")
            exit()

        filename = out.split(fs)[-1]
        if fs in out:
            _out = out.split(fs)
            _out.pop(-1)
            out_path = fs.join(_out)
        else:
            out_path = "."

        os.makedirs(out_path, exist_ok=True)    

        status = os.system(f'{config.ffmpeg_path} -i "{inp}" "{out}" {"" if args.verbose else "-hide_banner -loglevel error"}')

        if status == 0:
            if out_path == ".":
                saved_txt = f"Saved as {color.bright_yellow}{filename}{color.bright_green}"
            else:
                saved_txt = f"Saved in {color.bright_yellow}{out_path}{color.bright_green} as {color.bright_yellow}{filename}{color.bright_green}"
            
            spinner.text = f"{color.bright_green}File converted successfully. {saved_txt}.{color.reset}"
            spinner.ok(f"✅")
        else:
            spinner.text = f"{color.red}Error occurred while converting {color.bright_yellow}{args.input}{color.reset}"
            spinner.fail(f"💥")