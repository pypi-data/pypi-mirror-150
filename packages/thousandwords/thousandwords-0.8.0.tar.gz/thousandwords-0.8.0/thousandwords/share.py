from cProfile import run
import json
import uuid
import sys
from posixpath import join as urljoin
from IPython import get_ipython
from IPython.display import display
from IPython.core.magic import (
  Magics,
  cell_magic,
  magics_class,
)
from nanoid import generate
from thousandwords.auth import CognitoAuth
from thousandwords.cli import login
from thousandwords_core.serializer import Serializer
from .status import Status
from .lint import resolveUndefined
from .client import Client
from .capture import CapturedIO
from .config import CONFIG

def add_dependency_injection_comment(vnames, lines):
  if len(vnames) > 0:
    lines = [
      '""" 1000words-autogen',
      f"Dependenc{'ies' if len(vnames) > 1 else 'y'} injected: {', '.join(vnames)}",
      '"""',
    ] + lines
  return lines

def get_version():
  major, minor, *_ = sys.version_info
  return f"{major}.{minor}"

def query_yes_no(question, default="yes"):
  valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
  if default is None:
    prompt = " [y/n] "
  elif default == "yes":
    prompt = " [Y/n] "
  elif default == "no":
    prompt = " [y/N] "
  else:
    raise ValueError("invalid default answer: '%s'" % default)

  while True:
    sys.stdout.write(question + prompt)
    choice = input().lower()
    if default is not None and choice == "":
      return valid[default]
    elif choice in valid:
      return valid[choice]
    else:
      sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

class CellLink:
  def __init__(self, id):
    self.url = urljoin(CONFIG.instance_url, f'c/{id}')
  def _repr_pretty_(self, p, cycle):
    p.text('\n' + self.url)

@magics_class
class ShareMagic(Magics):
  def __init__(self, shell):
    Magics.__init__(self, shell=shell)

  @cell_magic("share")
  def cmagic(self, line="", cell=""):
    lines = cell.split('\n')
    try:
      undefs = resolveUndefined(cell)
    except Exception as e:
      print(e, file=sys.stderr)
      return
    
    client = Client()
    def puts3(name, data):
      with Status(f"Uploading dependency '{name}'"):
        return client.upload(str(uuid.uuid4()), data)
    srz = Serializer(puts3)
    vnames = list(set([u.message_args[0] for u in undefs]))

    varstr = ', '.join([f"'{v}'" for v in vnames])
    question = f"This will upload {varstr} server-side. Anyone with the link will have read access. Do you wish to proceed ?"
    if not query_yes_no(question, default="no"):
      print("Aborted")
      return

    for vname in vnames:
      try:
        obj = self.shell.user_ns[vname]
      except KeyError:
        print(f"Dependency '{vname}' is not defined", file=sys.stderr)
        return
      try:
        srz.add(vname, obj)
      except Exception as err:
        print(f"Could not serialize {vname}: {err}", file=sys.stderr)
        return

    lines = add_dependency_injection_comment(vnames, lines)
    run_request = {"lines": lines, "userNS": srz.ns, "version": get_version()}
    try:
      with Status("Executing cell remotely"):
        run_reply = client.run_cell(run_request)
    except Exception as err:
      print(err, file=sys.stderr)
      return

    if len(run_reply['userNS']) > 0:
      vnames = [v['name'] for v in run_reply['userNS']]
      print(f"Variable{'s' if len(vnames) > 1 else ''} captured: {', '.join(sorted(vnames))}")

    try:
      id = client.create_cell({
        "id": generate(size=11),
        "executeRequest": run_request,
        "executeReply": run_reply,
      })
    except Exception as err:
      print(err, file=sys.stderr)
      return

    display(CellLink(id))

get_ipython().register_magics(ShareMagic)
