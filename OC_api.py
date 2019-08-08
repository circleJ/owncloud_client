#!/usr/bin/env python      
# -*- coding: utf-8 -*-

import  owncloud,request
login_url = 'http://10.20.30.25'
user_name = 'admin'
user_pass = 'admin'

#
of = owncloud.FileInfo
class rewrite_oc(object):
    def __init__(self,login_url=None, user_name=None, user_pass=None):
        # 
        self.oc = owncloud.Client(login_url)
        self.oc.login(user_name, user_pass)
    def file_info(self,file_path):
        self.file_content = self.oc.file_info(file_path)
        _f_info = {}
        _f_info['file_path'] = of.get_path(self.file_content)
        _f_info['file_name'] = of.get_name(self.file_content)
        _f_info['file_modify'] = of.get_last_modified(self.file_content)
        _f_info['file_type'] = of.get_content_type(self.file_content)
        _f_info['file_size'] = of.get_size(self.file_content)
        return _f_info

    def _file_list(self,file_path='/'):
        whole_rets = self.oc.list(file_path, depth=1)
        nums = len(whole_rets)
        ret = []
        for i in range(nums):
            ret.append(of.get_name(whole_rets[i]))
        return nums,ret
    def _whole_file(self):
        whole_rets = self.oc.list('/', depth='infinity')
        nums = len(whole_rets)
        ret = []
        for i in range(nums):
            ret.append(of.get_name(whole_rets[i]))
        return ret
    def _whole_rets(self):
        whole_rets = self.oc.list('/', depth='infinity')
        nums = len(whole_rets)
        ret = []
        for i in range(nums):
            ret.append(of.get_context(whole_rets[i]))
        return ret

    def is_dir(self,file_path):
        file_content = self.oc.file_info(file_path)
        ret = of.is_dir(file_content)
        return ret

    def get_dir_zip(self,remote_path,local_filename):
        #
        self.oc.get_directory_as_zip(remote_path,local_filename)
    #
    def get_file(self,remote_file,local_file=None):
        self.oc.get_file(remote_file,local_file)
    #
    def _put_file(self,target_path, local_source_file):
        return self.oc.put_file(target_path, local_source_file)
    # 
    def _put_directory(self,remote_path, local_directory):
        return self.oc.put_directory(remote_path, local_directory)
    # 
    def _get_process(self):
        return self.oc.get_upload_progress()

    def _share_file_link(self,file_path, **kwargs):
        return self.oc.share_file_with_link(file_path,**kwargs)


if __name__ == '__main__':
    pass