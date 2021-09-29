pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'how_far')
gnome = import('gnome')

gnome.compile_resources('how_far',
  'how_far.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'how_far.in',
  output: 'how_far',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

how_far_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]
install_subdir('gps', install_dir: moduledir)
install_subdir('conversion', install_dir: moduledir)
install_data(how_far_sources, install_dir: moduledir)
