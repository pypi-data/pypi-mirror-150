# -*- coding: utf-8 -*-
# module transform_render_template.py
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
import os                                         #
import pluginlib                                  #
import parscival_plugins.transform                #
import logging                                    #
from pathlib import Path                          #
log = logging.getLogger(__name__)                 #
# ---------------------------------------------------------------------------
import jinja2                                     #
# ---------------------------------------------------------------------------
class RenderTemplate(parscival_plugins.transform.Processor):

  _alias_ = 'render_template'
  _version_ = '1.0.2'

  @staticmethod
  def process(parsing_spec, parsing_data, output_info, **params):
    """render the template in output_info using parsing_data

    Args:

    Returns:
      Boolean: NBIB Parsing data was transformed
    """
    # if a type tranformation is requested
    if output_info['type'] is not None:
      try:
        templates_path = os.getenv('PARSCIVAL_PLUGIN_RENDER_TEMPLATE_DIR',
                                   Path(parsing_spec['file'].name).parent)
        log.debug("Loading templates from '%s'", templates_path)
        # @ see https://stackoverflow.com/a/38642558/2042871
        templateLoader = jinja2.FileSystemLoader(searchpath = templates_path)
        templateEnv = jinja2.Environment(loader=templateLoader, autoescape=False)

        # render template directly into the output file
        log.info("Rendering template '%s'", params['template'])
        log.info("Storing output data on [yellow]{}[/yellow]".format(output_info['file']))
        template = templateEnv.get_template(params['template'])
        template.stream(parsing_data=parsing_data).dump(str(output_info['file']))

      except jinja2.exceptions.TemplateError as e:
        log.error("Template [yellow]{}[/yellow] error: {}".format(
                           params['template'], type(e).__name__, e.__doc__))
        return False
      except Exception as e:
        log.error("Unknown error while rendering output for '{}': {} - {}".format(
                           output_info['type'], type(e).__name__, e.__doc__))
        return False

    return True
