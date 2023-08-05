# -*- coding: utf-8 -*-
# module worker.py
#
# Copyright (c) 2021  CorTexT Platform
# Copyright (c) 2021  Cogniteva SAS
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# ---------------------------------------------------------------------------
__doc__ = """
Worker for Parscival - methods to parse and transform datasets
=============================================================================

This module implements a generic approach to parse and
transform datasets according to a parsing specification
"""
__author__  = "Cristian Martinez, Lionel Villard"
__license__ = "MIT"
from parscival import __version__
# ---------------------------------------------------------------------------
import pluginlib                                 #

import argparse                                  #
import logging                                   #
import logging.handlers                          #
import sys                                       #
import os                                        #

import contextlib                                #
import mmap                                      #
import re                                        #

import yaml                                      #
import site                                      #

import klepto                                    #

from pathlib import Path                         #

from rich.logging import RichHandler             #
from rich.console import Console                 #
from rich.theme import Theme                     #
from rich.text import Text                       #

from rich.panel import Panel                     #
from rich.rule import Rule                       #
from rich.syntax import Syntax                   #
from rich.table import Table                     #

from parsimonious.grammar import Grammar         #
from parsimonious.nodes import NodeVisitor       #
from parsimonious.exceptions import ParseError   #

from rich.progress import (                      #
  BarColumn,                                     #
  Progress,                                      #
  SpinnerColumn,                                 #
  TextColumn,                                    #
  TimeElapsedColumn,                             #
  TimeRemainingColumn,                           #
)

from contextlib import suppress                  #
from dotenv import load_dotenv                   #
# ---------------------------------------------------------------------------
log = logging.getLogger(__name__)

# short log levels names
# according to the RCF5424
# @see https://datatracker.ietf.org/doc/html/rfc5424
logging.addLevelName(logging.DEBUG,    "(%%)")
logging.addLevelName(logging.INFO,     "(II)")
logging.addLevelName(logging.WARNING,  "(WW)")
logging.addLevelName(logging.ERROR,    "(EE)")
logging.addLevelName(logging.CRITICAL, "(CC)")
logging.addLevelName(logging.NOTSET,   "(--)")

# create a custom logging theme
# level names must be in lowercase
log_theme = Theme({
  "repr.number": "bold blue",
  "logging.level.(%%)": "green",
  "logging.level.(ii)": "blue",
  "logging.level.(ww)": "blue",
  "logging.level.(ee)": "red",
  "logging.level.(cc)": "red",
  "logging.level.(@@)": "red",
  "logging.level.(--)": "white"
})

# setup rich console for logging
console = Console(
  record=True,
  theme=log_theme)
# ---------------------------------------------------------------------------

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from parscival.main import process_datasets`,
# when using this Python module as a library.

def load_datasets_info(parsing_spec, parsing_data, file_datasets):
  """Get metadata about the documents to parse
  """
  log.info("Getting documents information...")
  records_total = 0
  files_total = 0

  # get the record separator from the parsing spec
  spec_identifier = (parsing_spec.get('spec', {})
                              .get('identifier', 'unknown'))

  # get the record separator from the parsing spec
  record_separator = (parsing_spec.get('spec', {})
                                  .get('grammar', {})
                                  .get('record_separator', None))

  # continue only if a record separator is defined
  if record_separator is None:
    log.error("[yellow]{}[/yellow] - undefined grammar.record_separator".format(spec_identifier))
    return False

  # compile the record separator as a regex
  record_separator_regex = re.compile(bytes(record_separator, encoding= 'utf-8'))

  # loop over each file
  for f in file_datasets:
    file_path = Path(f.name)
    filename  = file_path.name

    # ensure that we have an existing non empty file
    if not file_path.exists() or file_path.stat().st_size == 0:
      log.warn("[cyan]{}[/cyan] is empty".format(filename))
      continue

    # @see https://stackoverflow.com/a/11692134/2042871
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    with contextlib.closing(mm) as dataset:
      records = record_separator_regex.findall(dataset)
      records_count = len(records)
      records_total = records_total + records_count
      files_total  += 1

      # update documents information
      parsing_data['datasets'].append({
        'file'     : f,
        'documents': [],
        'filename' : filename,
        'shortname': os.path.basename(filename),
        'stats' : {
          'total'    : records_count,
          'parsed'   : 0,
          'missed'   : 0,
          'lines'    : 0
        }
      })

    log.info("[cyan]{}[/cyan] - found {} documents".format(filename, records_count))

  # report about the number of documents and files to parse
  log.info("Preparing to parse {} documents from {} files".format(records_total,
                                                    len(parsing_data['datasets'])))

  # update the number of documents
  parsing_data['stats']['total'] = records_total
  parsing_data['stats']['files'] = files_total

  return True

def get_parsing_spec(file_parsing_spec):
  """Get the parscival specification including grammar
  """
  parsing_spec  = {
    'spec' : { },
    'valid': True
  }

  try:
    parsing_spec['spec'] = yaml.safe_load(file_parsing_spec)
    parsing_spec['file'] = file_parsing_spec

    # shorthand for the type of grammar
    grammar_type = parsing_spec['spec']['grammar']['type']

    if grammar_type == 'PEG':
      # parsing expression grammar (PEG)
      # space = O(grammar size * text length)
      # complexity = O(text length)
      parsing_spec['grammar'] = Grammar(parsing_spec['spec']['grammar']['rules'])
    else:
      raise ValueError("Unknown grammar type '{}'".format(grammar_type))

  except yaml.YAMLError as e:
    log.error("Error while parsing spec {}".format(str(e.problem_mark).strip()))
    parsing_spec['valid'] = False
  except Exception as e:
    log.error("Error loading the parscival specification from '{}': {} - {}".format(
    Path(file_parsing_spec.name).name, type(e).__name__, e.__doc__))
    parsing_spec['valid'] = False

  return parsing_spec

def map_parsed_tree(parsing_spec, dataset_info, document_info):
  """process the document tree

  Args:

  Returns:
    Text: Parscival Parsing Keys
  """
  print(document_info['keys'][0])
  return

def process_document_tree(parsing_spec, dataset_info, document_info):
  """process the document tree

  Args:

  Returns:
    Text: Parsed Keys - Values
  """
  class KeyValueVisitor(NodeVisitor):
    def visit_dataset(self, node, visited_children):
      """ Gets the dataset. """
      documents = visited_children
      return documents

    def visit_document(self, node, visited_children):
      """ Gets the document. """
      _, record_start, record_members, record_end, = visited_children
      record_members.insert(0,record_start)
      record_members.append(record_end)
      return [r for r in record_members if r is not None]

    def visit_record_member(self, node, visited_children):
      """ Returns a key-value pair. """
      key, _, value, *_ = node.children

      # common processing for any value
      custom_value_text = value.text.strip()
      custom_value_text = re.sub(r'\n +', ' ', custom_value_text)
      custom_value_text = re.sub(r'  +', ' ',  custom_value_text)

      # only process requested keys
      if (parsing_spec['spec']['options']['only_requested_keys'] == False or
         key.text in parsing_spec['spec']['keys']):
        return key.text, custom_value_text

      # mark this member as not to be used
      return None

    def visit_record_start(self, node, visited_children):
      """ Returns record start. """
      return self.visit_record_member(node, visited_children)

    def visit_record_end(self, node, visited_children):
      """ Returns record end. """
      return self.visit_record_member(node, visited_children)

    def generic_visit(self, node, visited_children):
      """ The generic visit method. """
      return visited_children or node

  visitor = KeyValueVisitor()
  return visitor.visit(document_info['tree'])

def parse_document(parsing_spec, dataset_info, document_info):
  """Parscival parse files

  Args:

  Returns:
    Tree: a parse tree of document_info['buffer']
  """
  try:
    document_tree = parsing_spec['grammar'].parse(document_info['buffer'])

  except ParseError as e:
    ## e.g. malformed document (line 227717)
    log.warning("[cyan]{}[/cyan] - malformed document (line {})".format(
                                      dataset_info['filename'],
                                      document_info['line']['start']))

    # e.g. rule: 'record_end' didn't match (line 227754, column 1)
    log.debug("[cyan]{}[/cyan] - rule: '{}' didn't match "
              "(line {}, column {})".format(
                         dataset_info['filename'],
                         e.expr.name,
                        (e.line() + document_info['line']['start'] - 1),
                         e.column()))
    return None

  except Exception as e:
    log.error(e)
    return None

  return document_tree

def parse_dataset(parsing_spec, dataset_info, main_task, main_progress):
  """parse files

  Args:

  Returns:
    Boolean: True if the parsing was successful, False otherwise
  """
  filename_short = dataset_info['filename'][:20]

  if dataset_info['stats']['total'] <= 0:
   log.warning("[cyan]{}[/cyan] - no documents found".format(filename_short))
   return False

  log.info("[cyan]{}[/cyan] - parsing...".format(filename_short))

  # show the progress of the current file parsing
  local_task = main_progress.add_task(
               "[green]Parsing {:<20s}".format(filename_short),
               total=dataset_info['stats']['total'])

  # parse document by document
  document_info  = {
    'buffer'  : "",
    'line': {
      'start': 0
    },
    'tree' : None
  }

  document_info['buffer'] = ""
  document_parsed_count = 0
  dataset_line_count = 0
  mm = mmap.mmap(dataset_info['file'].fileno(), 0, access=mmap.ACCESS_READ)
  with contextlib.closing(mm) as dataset:
    for line in iter(dataset.readline, b""):
      # as mmap file is open in read bynary (r+b) mode we need to
      # decode it as UTF-8 to use match() and parse()
      line = line.decode('utf-8')

      # increment the number of lines processed
      dataset_line_count = dataset_line_count + 1

      # for suppress(Exception):
      # @see https://stackoverflow.com/a/15566001/2042871

      # START
      try:
        if parsing_spec['grammar']['record_start'].parse(line):
          # test if we have a document buffer to process
          if len(document_info['buffer']) > 0:
            # try to parse the document
            document_info['tree'] =  parse_document(parsing_spec,
                                                    dataset_info,
                                                    document_info)
            # check if the document was successfully parsed
            if document_info['tree'] is not None:
              # process the document tree and create a list of tuples
              # of type (key, value)
              # [0]: as we are parsing a single document
              dataset_info['documents'].append(process_document_tree(parsing_spec,
                                                                    dataset_info,
                                                              document_info)[0])
              # and then update the progress
              document_parsed_count = document_parsed_count + 1
              main_progress.update(main_task, advance=1)
              main_progress.update(local_task, advance=1)

          # reinitialize the document buffer
          document_info['buffer'] = line
          document_info['line']['start'] = dataset_line_count
          continue

      except ParseError as e:
        pass

      except Exception as e:
        log.error(e)
        return False

      # MEMBER OR END
      document_info['buffer'] = document_info['buffer'] + line

    # try to parse the last document
    # this is because above documents are only parsed whenever
    # a new document is found
    if len(document_info['buffer']) > 0:
      # try to parse the document
      document_info['tree'] =  parse_document(parsing_spec,
                                              dataset_info,
                                              document_info)
      # check if the document was successfully parsed
      if document_info['tree'] is not None:
        # process the document tree and create a list of tuples
        # of type (key, value)
        # [0]: as we are parsing a single document
        dataset_info['documents'].append(process_document_tree(parsing_spec,
                                                              dataset_info,
                                                         document_info)[0])
        # and then update the progress
        document_parsed_count = document_parsed_count + 1
        main_progress.update(main_task, advance=1)
        main_progress.update(local_task, advance=1)

  # update the number of the documents found
  dataset_info['stats']['parsed'] = document_parsed_count

    # update the number of lines scanned
  dataset_info['stats']['lines'] = dataset_line_count

  # document with errors
  document_error_count  = 0

  # documents parsed
  log.info("[cyan]{}[/cyan] - {} of {} documents were parsed".format(
                                                   dataset_info['filename'],
                                                   dataset_info['stats']['parsed'],
                                                   dataset_info['stats']['total']))
  # documents missed
  dataset_info['stats']['missed'] = (dataset_info['stats']['total'] -
                                    (dataset_info['stats']['parsed'] + document_error_count))

  # if we found less documents than expected
  if dataset_info['stats']['missed'] > 0:
    # update progress to reflect the number of missed documents
    main_progress.update(main_task, advance=dataset_info['stats']['missed'])
    main_progress.update(local_task, advance=dataset_info['stats']['missed'])
    log.warning("[cyan]{}[/cyan] - {} malformed documents were missing".format(
                                             dataset_info['filename'],
                                             dataset_info['stats']['missed']))
  # lines scanned
  log.info("[cyan]{}[/cyan] - {} lines scanned".format(dataset_info['filename'],
                                                       dataset_info['stats']['lines']))

  return True

def get_plugins_loader(plugin_group):
  """get the pluginlib interface to import and access plugins of a targeted type

  Args:
    plugin_group(str): Retrieve plugins of a group ('transform', 'mapping', ...)

  Returns:
    Class: Interface for importing and accessing plugins
  """
  # get the plugin loader
  loader = pluginlib.PluginLoader()

  # return early if the group is already loaded
  if loader is not None and plugin_group in loader.plugins:
    return loader

  try:
    # get the semicolon delimited list of paths from environment
    plugins_paths = os.getenv('PARSCIVAL_PLUGINS_PATHS')

    # create a list of paths
    if plugins_paths is not None:
      plugins_paths = plugins_paths.split(';')
    else:
      plugins_paths = []

    # compute a fallback path relative to project
    plugins_fallback_path = str(Path.joinpath(
                              Path(__file__).parent.parent.relative_to
                              (Path(__file__).parent.parent.parent),
                              'parscival_plugins'))
    plugins_paths.insert(0, plugins_fallback_path)

    # add some extra paths from site-packages directories
    for path in site.getsitepackages():
      plugins_paths.insert(0, str(Path.joinpath(Path(path), 'parscival_plugins')))

    # append the plugin type to each of paths
    plugins_type_paths = [ os.path.join(p, plugin_group) for p in plugins_paths ]
    # remove non-existing paths
    plugins_type_paths = [ p for p in plugins_type_paths if os.path.isdir(p) ]

    # test if there is at least one valid path
    if not plugins_type_paths:
      log.error("There are not valid paths pointed out by '%s'",
                'PARSCIVAL_PLUGINS_PATHS')
      return None

    # recursively load plugins from paths
    loader = pluginlib.PluginLoader(paths = plugins_type_paths)

  except pluginlib.PluginImportError as e:
      if e.friendly:
        log.error("{}".format(e))
      else:
        log.error("Unexpected error loading %s plugins", plugin_group)
      return None

  # and return loader
  return loader

def map_parsed_data(parsing_spec, parsing_data):
  """map an already parsed dataset according to a spec

  Args:

  Returns:
    Boolean: True if the mapping is successful, False otherwise
  """
  # try to load plugins
  plugin_group = 'mapping'
  loader  = get_plugins_loader(plugin_group)

  # exit early if we failed to get the interface of the loader
  if loader is None: return False

  # get the nested dictionary of plugins
  plugins = loader.plugins

  if not 'mappings' in parsing_spec['spec']:
    log.error("No key 'mappings' found in the given parsing spec")
    return False

  # first check if all the requested plugins are avalaible
  # this is done only once per execution
  for key in parsing_spec['spec']['mappings']:
    for mapping in parsing_spec['spec']['mappings'][key]:
      # only if we have a plugins key
      if 'plugins' not in mapping or mapping['plugins'] is None: continue

      # get the group and name of the requested plugin
      for plugin_call in mapping['plugins']:
        plugin_group  = list(plugin_call.keys())[0]
        plugin_name   = list(plugin_call.values())[0]
        plugin_id = "{}.{}".format(plugin_group,plugin_name)
        # test if plugin exists
        if plugin_group not in plugins or plugin_name not in plugins[plugin_group]:
          log.error("Requesting to call an unknown plugin '{}' when mapping key '{}'".format(
                    plugin_id, key))
          return False

  # loop over datasets and documents
  file_id = 0
  document_id = 0
  for dataset_info in parsing_data['datasets']:
    # loop over parsed documents
    for document in dataset_info['documents']:
      document_key_rank_id = {}
      # loop over key-values
      for key, value in document:
        # loop over key mappings
        for mapping in parsing_spec['spec']['mappings'][key]:
          # key to create
          map_key = mapping['target']

          # check if the rank key is defined by the current mapping key
          # or if it depends on a key referenced by the 'rank' attribute
          rank_key = mapping['rank'] if 'rank' in mapping else map_key

          # check if we need to initialize the rank id counter for this key
          if not rank_key in document_key_rank_id:
            document_key_rank_id[rank_key] = 0
          # increase the rank id counter for this key
          elif map_key == rank_key:
            document_key_rank_id[rank_key] = document_key_rank_id[rank_key] + 1

          # get the current rank id
          rank_id = document_key_rank_id[rank_key]

          # check if we need to initialize the mappings for this key
          if not map_key in parsing_data['mappings']:
            parsing_data['mappings'][map_key] = []

          # create a list of nodes with a default node row
          nodes = [
            {
              'file'       : dataset_info['shortname'],
              'id'         : document_id,
              'rank'       : rank_id,
              'parserank'  : 0,
              'data'       : value
            }
          ]

          # call requested plugins
          if 'plugins' in mapping and mapping['plugins'] is not None:
            for plugin_call in mapping['plugins']:
              plugin_group  = list(plugin_call.keys())[0]
              plugin_name   = list(plugin_call.values())[0]
              plugin_id = "{}.{}".format(plugin_group,plugin_name)
              plugin = plugins[plugin_group][plugin_name]
              # call the process function of each plugin
              log.debug("Calling plugin '[green]{}[/green]' for key '{}' in " \
                        "document {}".format(plugin_id, key, document_id))
              params = plugin_call['params'] if 'params' in plugin_call  else {}
              if not plugin.process(parsing_spec, parsing_data, nodes, **params):
                log.warn("Plugin '{}' finished with issues for key '{}' and nodes: {}".format(
                          plugin_id, key, nodes))

          # add the mapped nodes for the current key
          parsing_data['mappings'][map_key].extend(nodes)

      # increase the document_id
      document_id = document_id + 1

    # increase file id
    file_id = file_id + 1

  return True

def curate_data(process_stage, parsing_spec, parsing_data):
  """curate data according to a spec

  Args:

  Returns:
    Boolean: True if the process is successful, False otherwise
  """

  # check if there are curation tasks to be performed
  if not 'curation' in parsing_spec['spec']:
    return True

  # check if there are curation tasks for this stage
  if not process_stage in parsing_spec['spec']['curation'] or \
    parsing_spec['spec']['curation'][process_stage] is None:
    return True

  # try to load plugins
  plugin_group = 'curation'
  loader  = get_plugins_loader(plugin_group)
  # exit early if we failed to get the interface of the loader
  if loader is None: return False

  # get the nested dictionary of plugins
  plugins = loader.plugins

  # first check if all the requested plugins are available
  for task_name in parsing_spec['spec']['curation'][process_stage]:
    task = parsing_spec['spec']['curation'][process_stage][task_name]
    if task is None or 'plugins' not in task or task['plugins'] is None: continue

    # loop for each plugin call of this task
    for plugin_call in task['plugins']:
      # get the type and name of the requested plugin
      plugin_type   = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}.{}".format(process_stage,plugin_type,plugin_name)
      # test if plugin exists
      if plugin_group not in plugins or plugin_id not in plugins[plugin_group]:
        log.error("Requesting to call an unknown plugin '{}' while curating mapped dataset".format(
                  plugin_id))
        return False

  # now loop for each task calling the requested plugins
  for task_name in parsing_spec['spec']['curation'][process_stage]:
    task = parsing_spec['spec']['curation'][process_stage][task_name]
    if task is None or 'plugins' not in task or task['plugins'] is None: continue

    # loop for each plugin call of this task
    for plugin_call in task['plugins']:
      # get the group and name of the requested plugin
      plugin_type   = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}.{}".format(process_stage,plugin_type,plugin_name)

      # get the request plugin
      plugin = plugins[plugin_group][plugin_id]

      # call the process function of this plugin
      log.debug("Calling plugin '[green]{}[/green]'".format(plugin_id))
      params = plugin_call['params'] if 'params' in plugin_call  else {}
      if plugin.process(parsing_spec, parsing_data, **params):
        log.debug("The execution of '{}' was successful".format(plugin_id))
      else:
        log.error("Plugin '{}' finished with errors".format(plugin_id))
        return False

  return True

def transform_parsed_data(parsing_spec,
                          parsing_data,
                          output_info):
  """transform parsed data

  Args:

  Returns:
    Boolean: True if the transform is successful, False otherwise
  """
  try:
    # try to load plugins
    plugin_group = 'transform'
    loader  = get_plugins_loader(plugin_group)

    # exit early if we failed to get the interface of the loader
    if loader is None: return False

    # get the nested dictionary of plugins
    plugins = loader.plugins

    # first loop to check if the requested plugins are available
    transform_type = output_info['type']
    for plugin_call in parsing_spec['spec']['outputs'][transform_type]['plugins']:
      plugin_group  = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}".format(plugin_group,plugin_name)
      # test if plugin exists
      if plugin_group not in plugins or plugin_name not in plugins[plugin_group]:
        log.error("Calling undefined plugin '{}' while processing output of type '{}'".format(
                  plugin_id, transform_type))
        return False

    # now we call each plugin following the declaration order
    log.info("Processing output of type '[green]{}[/green]'".format(transform_type))
    for plugin_call in parsing_spec['spec']['outputs'][transform_type]['plugins']:
      plugin_group  = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}".format(plugin_group,plugin_name)
      plugin = plugins[plugin_group][plugin_name]
      # call the process function of each plugin
      log.debug("Calling plugin '[green]{}[/green]'".format(plugin_id))
      params = plugin_call['params'] if 'params' in plugin_call  else {}
      if plugin.process(parsing_spec, parsing_data, output_info, **params):
        log.debug("The execution of '{}' was successful".format(plugin_id))
      else:
        log.error("Plugin '{}' finished with errors".format(plugin_id))
        return False

  except pluginlib.PluginImportError as e:
      if e.friendly:
        log.error("{}".format(e))
      else:
        log.error("Unexpected error loading %s plugins", plugin_group)
      return False

  return True

def process_datasets(file_parsing_spec, file_output, file_datasets):
  """Parscival parse files

  Args:

  Returns:
    Boolean: True if data was parsed, False otherwise
  """
  # first get the parsing specification
  parsing_spec = get_parsing_spec(file_parsing_spec)
  if parsing_spec['valid'] == False or not 'spec' in parsing_spec:
    log.critical("The parscival specification is not valid")
    return False

  # check the type of the output to create
  # /path/to/foo.bar.zaz
  # foo
  output_name  = file_output.with_suffix('').stem
  # bar.zaz
  output_extension = file_output.name[len(output_name)+1:]

  # keep track about the requested output
  output_info  = {
    'type' : None,
    'file': file_output
  }

  # by default we need to create a hdf5
  parsing_data_output_file = str(Path.joinpath(file_output.parent, output_name + '.hdf5'))
  log.info("Storing parsing data on [yellow]{}[/yellow]".format(parsing_data_output_file))

  # only .hdf5 and spec tranforms format types are valid
  if output_extension != 'hdf5':
    # eg. cortext.json or cortext.db
    output_info['type'] = output_extension
    if not output_extension in parsing_spec['spec']['outputs']:
      log.critical("A valid output type is required to continue")
      log.critical("Requested output type: [yellow].{}[/yellow]"
                   .format(output_extension))
      log.critical("The known output types are: [yellow][.hdf5; .{}][/yellow]"
                   .format('; .'.join(parsing_spec['spec']['outputs'])))
      return False

  # initial dictionary to seed the hdf5 parsing_data
  parsing_data_init_dict  = {
    'datasets' : [],
    'mappings' :  {},
    'stats' : {
      'total'    : 0,
      'parsed'    : 0,
      'missed'   : 0,
      'lines'    : 0,
      'files'    : 0
    }
  }

  # ensure to have an empty output file
  open(parsing_data_output_file, 'w').close()

  # initialize a dictionary with a single hdf5 file archive backend
  parsing_data = klepto.archives.hdf_archive(
                  parsing_data_output_file,
                  dict = parsing_data_init_dict,
                  cached = True,
                  meta = True)

  # only continues if we have a valid parsing specification
  if not parsing_spec['valid']:
    log.critical("A valid parsing specification is required to continue")
    return False

  # then get information about the datasets to process
  if not load_datasets_info(parsing_spec, parsing_data, file_datasets):
    log.critical("It was not possible to obtain any information about the datasets")
    return False

  # visualize progress on the console
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeRemainingColumn(),
    TimeElapsedColumn(),
    console=console,
    transient=True,
  ) as progress:
    log.info("Starting parsing process...")
    log.info("Using [yellow]{}[/yellow] v{} parsing specification".format(
             parsing_spec['spec']['identifier'],
             parsing_spec['spec']['version']))

    dataset_parsing_task = progress.add_task("[green]Parsing files",
                           total=parsing_data['stats']['total'])

    # parse each dataset
    for dataset_info in parsing_data['datasets']:
      if parse_dataset(parsing_spec, dataset_info, dataset_parsing_task, progress):
        # update stats
        parsing_data['stats']['parsed']  += dataset_info['stats']['parsed']
        parsing_data['stats']['missed'] += dataset_info['stats']['missed']
        parsing_data['stats']['lines']  += dataset_info['stats']['lines']

    # check if there is at least 1 parsed document
    if parsing_data['stats']['parsed'] <= 0:
      log.error("No documents parsed. Nothing to do!")
      return False

    # log global stats if multiple files
    if parsing_data['stats']['files'] > 1:
      # total parsed
      log.info("{} of {} documents were parsed".format(parsing_data['stats']['parsed'],
                                                       parsing_data['stats']['total']))
      # total missed
      if parsing_data['stats']['missed'] > 1:
        log.info("{} malformed documents were missing".format(parsing_data['stats']['missed']))

      # lines scanned
      log.info("{} lines scanned".format(parsing_data['stats']['lines']))

    # curate parsed data according to the spec
    if not curate_data('before_mapping', parsing_spec, parsing_data):
      log.error("Unexpected error curating mapped data")
      return False

    # map whole parsed data according to the spec
    if not map_parsed_data(parsing_spec, parsing_data):
      log.error("Unexpected error mapping parsed data")
      return False

    # curate mapped data according to the spec
    if not curate_data('after_mapping', parsing_spec, parsing_data):
      log.error("Unexpected error curating mapped data")
      return False

    # dump from the cache to the archive representing the parsed data
    parsing_data.dump()

    # transform whole parsed data according to the requested output type
    if not transform_parsed_data(parsing_spec,
                                parsing_data,
                                output_info):
      log.error("Unexpected error transforming parsed data")
      return False

    if not progress.finished:
      log.error("Unexpected error")
      return False

    log.info("Parsing process successfully completed...")
    return True

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="""
    A modular framework for parsing, mapping and transforming data
    """)
    parser.add_argument(
        "--version",
        action="version",
        version="parscival {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="file_parsing_spec",
        help="parscival specification",
        type=argparse.FileType('r'),
        metavar="FILE_PARSER_SPEC")
    parser.add_argument(
        dest="file_output",
        help="parsed data output",
        type=lambda p: Path(p).absolute(),
        metavar="FILE_OUTPUT")
    parser.add_argument(
        dest="file_datasets",
        help="input dataset",
        type=argparse.FileType('r+b'),
        metavar="FILE_DATASET",
        nargs='+')
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.INFO
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    # setup the logger rich handler
    rh = RichHandler(
        console=console,
        enable_link_path=False,
        markup=True,
        omit_repeated_times=False,
        rich_tracebacks=True,
        show_level=False,
        show_path=False,
        show_time=False
      )

    # and finally the logger
    # TODO(martinec) For CorText Manager Add 'file' handler here
    logging.basicConfig(
        level=loglevel, format="%(asctime)s %(levelname)s %(message)s", datefmt="[%X]",
        handlers=[rh]
    )

def main(args):
    """Wrapper allowing :func:`parse` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`parse`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    # take environment variables from .env
    load_dotenv()
    # parse arguments
    args = parse_args(args)
    # setup logging at level
    setup_logging(args.loglevel)

    log.info("Starting the worker...")

    if process_datasets(args.file_parsing_spec, args.file_output, args.file_datasets):
      log.info("Worker finished without errors")
    else:
      log.critical("Worker finished with errors")

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function is used as entry point to create a console script with setuptools.
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run this Python
    # module as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m parscival.worker PARAMS...
    #
    run()
