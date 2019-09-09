import requests, json, os

# shared
default_size = '600,' # iiif formatted size - https://iiif.io/api/image/2.1/#image-request-uri-syntax
default_out_dir = 'iiif-downloads'
default_verbose = True

class Manifest:
  def __init__(self, *args, **kwargs):
    self.id = ''
    self.json = {}
    self.images = []
    self.verbose = kwargs.get('verbose', default_verbose)
    self.out_dir = kwargs.get('out_dir', default_out_dir)
    self.size = kwargs.get('size', default_size)
    if kwargs.get('url', False):
      self.load_from_url(kwargs.get('url'))
    self.make_out_dirs()

  def make_out_dirs(self):
    '''Make the output directories in which saved data is stored'''
    for i in ['manifests', 'images', 'metadata']:
      out_dir = os.path.join(self.out_dir, i)
      if not os.path.exists(out_dir):
        os.makedirs(out_dir)

  def load_from_url(self, url):
    '''Load a IIIF manifest from a url'''
    if self.verbose: print(' * loading manifest from url', url)
    self.json = requests.get(url).json()
    self.id = self.json.get('@id', '').split('/')[-1].rstrip('.json')

  def json_present(self):
    if not self.json:
      print(' ! please use the load_from_url(path_to_manifest) method before calling this method')
      return False
    return True

  def save(self):
    '''Save self.json to disk'''
    if self.json_present():
      out_path = os.path.join(self.out_dir, 'manifests', self.id)
      save_json(out_path, self.json, verbose=self.verbose)

  def save_images(self):
    '''Save self.json and all associated images to disk'''
    if self.json_present():
      self.save()
      # save all images in this manifest
      for i in self.json.get('sequences', []):
        for j in i.get('canvases', []):
          for k in j.get('images', []):
            url = k['resource']['@id']
            self.images.append(Image(size=self.size, url=url, out_dir=self.out_dir, verbose=self.verbose))
    for i in self.images:
      i.save()

class Image:
  def __init__(self, *args, **kwargs):
    self.json = {}
    self.id = ''
    self.img = None
    self.url = kwargs.get('url', None)
    self.size = kwargs.get('size', default_size)
    self.out_dir = kwargs.get('out_dir', default_out_dir)
    self.verbose = kwargs.get('verbose', default_verbose)
    if self.url:
      self.load_from_url()

  def load_from_url(self, *args):
    '''Load a IIIF image from a url'''
    url = args[0] if len(args) else self.url
    url = self.format_url(url)
    if self.verbose: print(' * loading image from url', url)
    self.id = url.split('/')[4]
    self.img = requests.get(url).content

  def format_url(self, url):
    '''Format the url to request an image of a reasonable size'''
    #{scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}
    #scheme, server, prefix, identifier, region, size, rotation, quality = [i for i in url.split('/') if i]
    split = url.split('/')
    split[-3] = self.size
    return '/'.join(split)

  def save(self):
    '''Save image to disk. NB: '''
    out_path = os.path.join(self.out_dir, 'images', self.id)
    if not out_path.endswith('.png'):
      out_path += '.png'
    if self.verbose: print(' * saving', out_path)
    with open(out_path, 'wb') as out:
      out.write(self.img)

def save_json(path, obj, verbose=default_verbose):
  if verbose:
    print(' * saving manifest to', path)
  if not path.endswith('.json'):
    path += '.json'
  if not os.path.exists(path):
    with open(path, 'w') as out:
      json.dump(obj, out)
  else:
    print(' ! refusing to overwrite content at location', path)
