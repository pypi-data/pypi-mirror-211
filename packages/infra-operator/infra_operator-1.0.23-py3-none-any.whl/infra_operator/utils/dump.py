import oyaml as yaml


def yaml_multiline_string_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        data = '\n'.join([line.rstrip() for line in data.strip().splitlines()])
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, yaml_multiline_string_presenter)


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def dump(data, stream=None):
    yaml.dump(data, stream, allow_unicode=True,
              Dumper=MyDumper, default_flow_style=False)
