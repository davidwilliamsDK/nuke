import os, sys, subprocess, glob, re

def get_shot_dir(path):
    '''
    Takes path and looks for s0000 and strips everything after the s0000 and returns it. 
    '''
    dir, file = os.path.split( path )
    dir_list = dir.split('/')
    for i in range(len(dir_list)):
        if dir_list[i] and dir_list[i][0].lower() == 's' and dir_list[i][1:4].isdigit():
            string =  '%s' % '/'.join(dir_list[0:i+1])
            return string

def process( cmd_line):
    '''
    Subprocessing, Returning the process.
    '''
    cmd = cmd_line.split(' ')
    proc = subprocess.Popen(cmd, 
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
    return proc
    
def render(path, framespeed):
    print '\n\t- Starting\n'
    path = path.strip()
    online_folder = '%s/published2D/compOut/DPX' % get_shot_dir(path)
    
    if not os.path.exists(online_folder):
        os.makedirs(online_folder)
    
    source_dir, source_file = os.path.split(path)
    
    name, number, extension = source_file.split('.')

    src = '%s/%s.%s.%s' % (source_dir, name, '%04d', extension)
    version = None
    seq = None
    sh = None
    overlay = ''
    for d in source_dir.split('/'):
        if len(d) >= 3:
            if d[0].lower() == 'v' and d[1].isdigit() and d[2].isdigit():
                version = d
            if d[0].lower() == 'q' and d[1].isdigit() and d[2].isdigit():
                seq = d
            if d[0].lower() == 's' and d[1].isdigit() and d[2].isdigit():
                sh = d
                
    print 'version:[', version, ']\n','sequence:[', seq, ']\n','shot:[', sh, ']\n'

    overlay += '-overlay matte 1.9 0.5 '
    overlay += '-overlay testtext %s 6 6 1 16 1 1 1 ' % (seq)
    overlay += '-overlay testtext %s %s 6 1 16 1 1 1 ' % (sh, len(sh) * 16)
    overlay += '-overlay testtext %s %s 6 1 16 1 1 1 ' % ( version, (len(sh) * 16)+(len(version) * 16))
    overlay += '-overlay frameburn 1 1 16 '
    
    # rvio src -outrgb, 
    dst = '%s/%s.%s.dpx' % (online_folder, name, '%04d')
    convert( src, '-outrgb', o=dst, fps=framespeed)
    '''
    QUICKTIME!
    print '\t- # extension -> quicktime\n'
    destination = '%s/%s.mov' % (online_folder, name)
    cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio -fps %s -v %s -codec H.264 -outkeyinterval 20 \ -outdatarate 2500000 -o %s %s' % (fps, file_path, destination, overlay)
    #cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio -fps %s -v %s -outsrgb -o %s %s' % (fps, file_path, destination, overlay)
    #cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio -fps 25 -vv %s -outsrgb -o %s' % (file_path, destination)
    print cmd, '\n'
    print process(cmd).communicate()[0], '\n'
    '''
    
    """print '\t- # extension -> dpx\n'
    destination = '%s/%s.%s.dpx' % (online_folder, name, '%04d')
    ##    cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio -v %s -outlog -o %s' % (file_path, destination)
    cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio -v -strictlicense %s -outsrgb -o %s' % (file_path, destination)
    print cmd, '\n'
    #print 'Disabled while testing frameburning on the quicktime.'
    print process(cmd).communicate()[0], '\n'
    
        # extension -> jpg
    #destination = '%s/%s.%s.%s' %(online_folder, name,'%04d', 'jpg')
    #cmd = '/dsPantry/Install/RV_Player/Linux/bin/rvio %s -outsrgb -o %s' % (file_path, destination)
    #print process(cmd).communicate()[0]"""

def convertStack(src, dst, tag, fps):
    cmd = 'rvio -fps %s -strictlicense %s %s -o %s' % (fps, src, tag, dst)
    print process(cmd).communicate()[0], '\n'

def convert(*args, **kwargs):
    string = 'rvio -strictlicense'
    
    for arg in args:
        string += ' %s' % (arg)
        
    for k, v in kwargs.items():
        string += ' -%s %s' % (k, v)
        
    print string, '\n'
    #print process(string).communicate()[0], '\n'
    print process( 'rvio -help').communicate()[0], '\n'
if __name__ == "__main__":
    '''
    Testing purpose 
    online('/dsPipe/Lego_Test/Film/Return_of_the_Scriptors/Q0010/S0010/Comp/CompOut/v001/LCEP5_Q0050_S0010.0001.exr')
    '''
    render(sys.argv[1], sys.argv[2]) 
    
