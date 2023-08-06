"""Hadoop, hive related
Doc:

    python $utilmy/sspark/src/util_hadoop.py  print_env_variable
    utilmy spark print_config



"""
import os,sys


def log(*s):
  print(*s, flush=True)




##################################################################################
def hadoop_print_config(dirout=None):
  """ Print configuration variable for Hadoop, Spark


  """
  names =[
    'SPARK_HOME',
    'HADOOP_HOME'


  ]

  dd= []
  for ni in names:
    dd.append( [ni, os.environ.get(ni, '') ] )

  ### Print configuration files on disk
  ### SPARK_HOME/conf/spark_env.sh
  
   



###############################################################################################################
def hdfs_ls(path, filename_only=False):
    from subprocess import Popen, PIPE
    process = Popen(f"hdfs dfs -ls -h '{path}'", shell=True, stdout=PIPE, stderr=PIPE)
    std_out, std_err = process.communicate()

    if filename_only:
       list_of_file_names = [fn.split(' ')[-1].split('/')[-1] for fn in std_out.decode().split('\n')[1:]][:-1]
       return list_of_file_names

    flist_full_address = [fn.split(' ')[-1] for fn in std_out.decode().split('\n')[1:]][:-1]
    return flist_full_address



def hdfs_isok(path):
    import os
    print( os.system( f'hdfs dfs -ls {path}' ) )
     
def hdfs_mkdir(op_path):
    res = os_system( f"hdfs dfs -mkdir -p '{local_path}'  '{hdfs_path}' ", doprint=True)

def hdfs_copy_local_to_hdfs(local_path, hdfs_path, overwrite=False):
    if overwrite: hdfs_rm_dir(hdfs_path)
    res = os_system( f"hdfs dfs -copyFromLocal '{local_path}'  '{hdfs_path}' ", doprint=True)

def hdfs_copy_hdfs_to_local(hdfs_path, local_path):
    res = os_system( f"hdfs dfs -copyToLocal '{hdfs_path}'  '{local_path}' ", doprint=True)

def hdfs_rm_dir(path):
    if hdfs_dir_exists(path):
        print("removing old file "+path)
        cat = subprocess.call(["hadoop", "fs", "-rm", path ])

def hdfs_dir_exists(path):
    return {0: True, 1: False}[subprocess.call(["hadoop", "fs", "-test", "-f", path ])]

def hdfs_file_exists(filename):
    ''' Return True when indicated file exists on HDFS.
    '''
    proc = subprocess.Popen(['hadoop', 'fs', '-test', '-e', filename])
    proc.communicate()

    if proc.returncode == 0:
        return True
    else:
        return False

def os_makedirs(path:str):
  """function os_makedirs in HDFS or local
  """
  if 'hdfs:' not in path :
    os.makedirs(path, exist_ok=True)
  else :
    os.system(f"hdfs dfs mkdir -p '{path}'")



############################################################################################################### 
def hdfs_pd_read_parquet(path=  'hdfs://user/test/myfile.parquet/', 
                 cols=None, n_rows=1000, file_start=0, file_end=100000, verbose=1, ) :
    """ Single Thread parquet file reading in HDFS
    Doc::
    
       Required HDFS connection
       conda install libhdfs3 pyarrow
       os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'
    """
    import pyarrow as pa, gc
    import pyarrow.parquet as pq
    hdfs = pa.hdfs.connect()    
    
    n_rows = 999999999 if n_rows < 0  else n_rows
    
    flist = hdfs.ls( path )  
    flist = [ fi for fi in flist if  'hive' not in fi.split("/")[-1]  ]
    flist = flist[file_start:file_end]  #### Allow batch load by partition
    if verbose : print(flist)
    dfall = None
    for pfile in flist:
        if not "parquet" in pfile and not ".db" in pfile :
            continue
        if verbose > 0 :print( pfile )            
                    
        arr_table = pq.read_table(pfile, columns=cols)
        df        = arr_table.to_pandas()
        del arr_table; gc.collect()
        
        dfall = pd.concat((dfall, df)) if dfall is None else df
        del df
        if len(dfall) > n_rows :
            break

    if dfall is None : return None        
    if verbose > 0 : print( dfall.head(2), dfall.shape )          
    dfall = dfall.iloc[:n_rows, :]            
    return dfall



def hdfs_download_parallel(from_dir="", to_dir="",  verbose=False, n_pool=1,   **kw):
  """  Donwload files in parallel using pyarrow
  Doc::

        path_glob: list of HDFS pattern, or sep by ";"
        :return:
  """
  import glob, gc,os
  from multiprocessing.pool import ThreadPool

  def log(*s, **kw):
      print(*s, flush=True, **kw)

  #### File ############################################
  import pyarrow as pa
  hdfs  = pa.hdfs.connect()
  flist = [ t for t in hdfs.ls(from_dir) ]

  def fun_async(x):
      hdfs.download(x[0], x[1])


  ######################################################
  file_list = sorted(list(set(flist)))
  n_file    = len(file_list)
  if verbose: log(file_list)

  #### Pool count
  if   n_pool < 1  :  n_pool = 1
  if   n_file <= 0 :  m_job  = 0
  elif n_file <= 2 :
    m_job  = n_file
    n_pool = 1
  else  :
    m_job  = 1 + n_file // n_pool  if n_file >= 3 else 1
  if verbose : log(n_file,  n_file // n_pool )

  pool   = ThreadPool(processes=n_pool)

  res_list=[]
  for j in range(0, m_job ) :
      if verbose : log("Pool", j, end=",")
      job_list = []
      for i in range(n_pool):
         if n_pool*j + i >= n_file  : break
         filei = file_list[n_pool*j + i]

         xi    = (filei,  to_dir + "/" + filei.split("/")[-1] )

         job_list.append( pool.apply_async(fun_async, (xi, )))
         if verbose : log(j, filei)

      for i in range(n_pool):
        if i >= len(job_list): break
        res_list.append( job_list[ i].get() )


  pool.close()
  pool.join()
  pool = None
  if m_job>0 and verbose : log(n_file, j * n_file//n_pool )
  return res_list

 






############################################################################################################### 
def os_system(cmd, doprint=False):
  """ os.system  and retrurn stdout, stderr values
  """
  import subprocess
  try :
    p          = subprocess.run( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
    mout, merr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')
    if doprint:
      l = mout  if len(merr) < 1 else mout + "\n\nbash_error:\n" + merr
      print(l)

    return mout, merr
  except Exception as e :
    print( f"Error {cmd}, {e}")



def date_format(datestr:str="", fmt="%Y%m%d", add_days=0, add_hours=0, timezone='Asia/Tokyo', fmt_input="%Y-%m-%d", 
                returnval='str,int,datetime'):
    """ One liner for date Formatter
    Doc::

        datestr: 2012-02-12  or ""  emptry string for today's date.
        fmt:     output format # "%Y-%m-%d %H:%M:%S %Z%z"

        date_format(timezone='Asia/Tokyo')    -->  "20200519" 
        date_format(timezone='Asia/Tokyo', fmt='%Y-%m-%d')    -->  "2020-05-19" 
        date_format(timezone='Asia/Tokyo', fmt='%Y%m%d', add_days=-1, returnval='int')    -->  20200518 


    """
    from pytz import timezone as tzone
    import datetime

    if len(str(datestr )) >7 :  ## Not None
        now_utc = datetime.datetime.strptime( str(datestr), fmt_input)       
    else:
        now_utc = datetime.datetime.now(tzone('UTC'))  # Current time in UTC

    now_new = now_utc + datetime.timedelta(days=add_days, hours=add_hours)

    if timezone != 'utc':
        now_new = now_new.astimezone(tzone(timezone))


    if   returnval == 'datetime': return now_new ### datetime
    elif returnval == 'int':      return int(now_new.strftime(fmt))
    else:                        return now_new.strftime(fmt)



###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()

