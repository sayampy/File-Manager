import click,os,shutil,glob,seedir,textwrap,stat
from datetime import datetime

@click.group(context_settings={'help_option_names':['-h','--help']})
def main():
  '''
  Thank You for choosing this File Managing Cli App
  there is many unique features that you should check out.
  Check out our docs on: https://github.com/file-manager
  '''

_=main.command

@_()
@click.argument('path',nargs=-1,type=click.Path(exists=False))
@click.option('--DIR_','-r',is_flag=True,default=False,required=False,show_default='file',help='used for make dirs')
def mk(path,dir_):
  '''
  help to Make files and dirs
  '''
  DIR_=dir_
  if DIR_==True:
    for p in path:                
       os.mkdir(p)
  elif DIR_==False:
    for _file in path:
      open(_file,'a').close()
  for p in path: click.secho(f'{p} CREATED',fg='green')

@_()
@click.argument('path',nargs=-1,type=click.Path(exists=True))
def rm(path):
  '''
  help to remove files and dirs
  '''
  for d in path:
    if os.path.isdir(d):
      shutil.rmtree(d)
    else:
      os.remove(d)
    click.secho(f'{d} REMOVED',fg='red')

@_()
@click.argument('src',nargs=-1,type=click.Path(exists=True))
@click.argument('dst',nargs=1)
def cp(src,dst):
  '''
  help to copy files and dirs
  '''
  for path in src:
    if os.path.isdir(path):
      shutil.copytree(path,dst)
    elif os.path.isfile(path):
      shutil.copy(path,dst)
  click.secho(f'{src} COPIED TO {dst}',fg='cyan')
  
@_()
@click.argument('src',nargs=-1,type=click.Path(exists=True))
@click.argument('dst',nargs=1)
def mv(src,dst):
  '''
  help to move files and dirs
  '''
  for path in src:
    if os.path.isdir(path):
      shutil.copytree(path,dst)
      shutil.rmtree(path)
    elif os.path.isfile(path):
      shutil.move(path,dst)
  click.secho(f'{src} MOVED TO {dst}',fg='cyan')

@_('open')
@click.argument('filename',type=click.Path(exists=True))
def _open(filename):
  '''
  help to open files in another window
  '''
  click.secho('opening {filename}..',bold=True)
  click.launch(os.path.abspath(filename),locate=True)

@_()
@click.argument('search_for_path',nargs=-1)
@click.option('--searching_path','-P', default='.', required=False,
help="For change root path of searching",show_default='Current Path',type=click.Path(exists=True))
def search(search_for_path, searching_path):
  '''
  help to search dir or file around a huge tree
  '''
  search_for_path=os.path.basename(' '.join(search_for_path))
  searching_path=os.path.abspath(searching_path)
  files=glob.glob(f'{searching_path}/**/*{search_for_path}*',recursive = True)
  if files==[]:
    click.UsageError('No File or Dir Found,try after change searching path').show()
  for file in files:
    print(file)

@_()
@click.argument('path',type=click.Path(exists=True))
def pstat(path):
  '''
  shows detailed status//information of a file
  '''
  st = os.stat(path)
  if os.path.isdir(path):
    st.st_type='dir'
  else:
    st.st_type='file'
  print('Pathname:',end=' ')
  click.secho(os.path.basename(os.path.abspath(path)), bold=True)
  print(' type:',st.st_type)
  print(' creator:',st.st_creator)
  print(' permissions:',stat.filemode(st.st_mode))
  print(' size:',st.st_size,'B')
  print(' last modified:', datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d-%H:%M'))
  print(' user id:',st.st_uid)
  print(' group id:',st.st_gid)

@_('tree')
@click.argument('path',default='.',required=False)
def _tree(path):
  '''
  shows any directory in tree structure
  '''
  path = os.path.abspath(path)
  try:
    seedir.seedir(path)
  except NotADirectoryError as e:
    click.UsageError('NotADirectory').show()

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output: 
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

@_()
@click.argument('path',default='.',required=False)
@click.option('--sort','-s',type=click.Choice(['a2z','z2a','stat','default'],case_sensitive=True),
default='default',required=False,help='Sort the dir list with choice')
def ls(path,sort):
  '''
  listing a directory. check the sort feature
  '''
  wrapper = textwrap.TextWrapper(width=click.get_terminal_size()[0])
  listr = os.listdir(path)
  print(f'sorted_by: {sort}')
  if sort=='a2z':
    wp = wrapper.wrap(' '.join(sorted(listr,key=str.lower)))
    click.echo('\n'.join(wp))
  elif sort=='z2a':
    wp = wrapper.wrap(' '.join(sorted(listr,reverse=True,key=str.lower)))
    click.echo('\n'.join(wp))
  elif sort=='stat':
    for file in listr:
      file=os.path.join(path,file)
      print(stat.filemode(os.stat(file).st_mode)
      , f'{bytesto(os.path.getsize(file),"k")} KB', 
      f"{datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d-%H:%M')}",
      file,sep='  ')
  else:
    print('\n'.join(wrapper.wrap(' '.join(listr))))

if __name__=='__main__':
  main()
