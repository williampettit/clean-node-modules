import os
import shutil
import sys
import time
from typing import Literal, NoReturn


CONFIRM_BEFORE_DELETE = True


YesOrNo = Literal["y", "n"]


def unreachable() -> NoReturn:
  assert False, "Unreachable"


def confirm(prompt: str) -> bool:
  while True:
    choice = input(f"(y/n) {prompt}: ").lower().strip()
    if (choice == "y") or (choice == "n"):
      return (choice == "y")
    print(f"{quote(choice)} is not a valid choice. Please confirm with either {quote("y")} or {quote("n")}.")
  unreachable()


def quote(string: str, style: str = "\"") -> str:
  return f"{style}{string}{style}"


def delete_node_modules(start_dir: str) -> None:
  print(f"Deleting {quote("node_modules")} directories in {quote(start_dir)} ...")

  start_time = time.time()
  num_dirs_removed = 0

  for (root, dirs, _) in os.walk(start_dir):
    if "node_modules" in dirs:
      node_modules_path = os.path.join(root, "node_modules")

      shorter_node_modules_path = node_modules_path.removeprefix(start_dir)

      print(f"Deleting: {quote(shorter_node_modules_path)} ...", end="\n" if CONFIRM_BEFORE_DELETE else " ")
      
      if (not CONFIRM_BEFORE_DELETE) or confirm(f"Delete {quote(shorter_node_modules_path)}"):
        shutil.rmtree(node_modules_path)

      else:
        print(f"Okay, skipping {quote(shorter_node_modules_path)}")

      print("Done!")

      num_dirs_removed += 1

  end_time = time.time()
  time_taken = end_time - start_time
  
  print(f"Deleted {num_dirs_removed} directories")
  print(f"Time spent: {time_taken:,.1f}s")


def usage() -> NoReturn:
  print(f"Usage: {sys.argv[0]} \"path-to-base-directory\"")
  sys.exit(1)


def main():
  if len(sys.argv) != 2:
    usage()

  base_directory = os.path.expanduser(sys.argv[1])
  delete_node_modules(base_directory)


if __name__ == "__main__":
  main()
