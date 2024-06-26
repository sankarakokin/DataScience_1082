# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2016.12.25 首发
   
Top Football，又称Top Quant for football-简称TFB
TFB极宽足彩量化分析系统，培训课件-配套教学python程序
@ www.TopQuant.vip      www.ziwang.com
QQ总群:124134140   千人大群 zwPython量化&大数据 

  
文件名:tfb_sys.py
默认缩写：import tfb_sys as tfsys
简介：Top极宽量化·足彩系统参数模块
 

'''
#

import sys,os,re
import arrow,bs4,random

import numpy as np
import pandas as pd
import tushare as ts
#import talib as ta

import matplotlib as mpl
from matplotlib import pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
#import multiprocessing
#

#
import numexpr as ne  

#
import zsys
import ztools as zt
import zpd_talib as zta



#-----------global.var&const
#gidDType={'gid':str,'jq':int,'sq':int,'rq':int,'kend':int}
gidNil=['','','','','','',  '-1','-1','0',  '0','-1','-1',  '','','']
gidSgn=['gid','gset','mplay','mtid','gplay','gtid', 'qj','qs','qr',  'kend','kwin','kwinrq', 'tweek','tplay','tsell']
#
poolNil=['','','','','','',  '-1','-1','0',  '0','-1','-1',  '','','', '0',0,0,0, '-9']
poolSgn=['gid','gset','mplay','mtid','gplay','gtid', 'qj','qs','qr',  'kend','kwin','kwinrq', 'tweek','tplay','tsell'
         ,'cid','pwin9','pdraw9','plost9'  , 'kwin_sta']
#

gxdatNil=['','','',  0,0,0,0,0,0,  0,0,0,0,0,0, 0,0, 0,0,0,0,0,0,
         '','','','','', '-1','-1','0','-1','-1', '','' ]
gxdatSgn=['gid','cid','cname',
  'pwin0','pdraw0','plost0','pwin9','pdraw9','plost9',
  'vwin0','vdraw0','vlost0','vwin9','vdraw9','vlost9',
  'vback0','vback9',
  'vwin0kali','vdraw0kali','vlost0kali','vwin9kali','vdraw9kali','vlost9kali',
  #
  'gset','mplay','mtid','gplay','gtid', 
  'qj','qs','qr','kwin','kwinrq',  
  'tweek','tplay']
#
retNil=['', 0,0,0,0, 0,0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0]
retSgn=['xtim', 'kret9','kret3','kret1','kret0',  'knum9','knum3','knum1','knum0',  'ret9','num9','nwin9', 'ret3','ret1','ret0',  'nwin3','nwin1','nwin0',  'num3','num1','num0']
#retNil=[0,0,0,0, 0,0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0]
#retSgn=['kret9','kret3','kret1','kret0',  'knum9','knum3','knum1','knum0',  'ret9','num9','nwin9', 'ret3','num3','nwin3', 'ret1','num1','nwin1', 'ret0','num0','nwin0']

#--bt.var  
btvarNil=['', 0,0,0,0, 0,0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0,   0,0,0, 0,0,0,'']
btvarSgn=['xtim', 'kret9','kret3','kret1','kret0',  'knum9','knum3','knum1','knum0',  'ret9','num9','nwin9', 'ret3','ret1','ret0',  'nwin3','nwin1','nwin0',  'num3','num1','num0'
          ,'v1','v2','v3','v4','v5','nday','doc']
  
#self.nsum,self.nwin,self.ndraw,self.nlost=0,0,0,0
#self.kwin,self.kdraw,self.klost=0,0,0
#-------------------
#
#us0='http://trade.500.com/jczq/?date='
#http://odds.500.com/fenxi/shuju-278181.shtml
#http://odds.500.com/fenxi/yazhi-278181.shtml
#http://odds.500.com/fenxi/ouzhi-278181.shtml
us0_gid='http://trade.500.com/jczq/?date='
us0_ext0='http://odds.500.com/fenxi/'
us0_extOuzhi=us0_ext0+'ouzhi-'
us0_extYazhi=us0_ext0+'yazhi-'
us0_extShuju=us0_ext0+'shuju-'
#
rdat0='/tfbDat/'
rxdat=rdat0+'xdat/'
rmdat=rdat0+'mdat/'
rmlib=rdat0+'mlib/' #ai.mx.lib.xxx

#rgdat=rdat0+'gdat/'
#
rghtm=rdat0+'xhtm/ghtm/'  #gids_htm,days
rhtmOuzhi=rdat0+'xhtm/htm_oz/'
rhtmYazhi=rdat0+'xhtm/htm_az/'
rhtmShuju=rdat0+'xhtm/htm_sj/'
#        

#---glibal.lib.xxx
gids=pd.DataFrame(columns=gidSgn,dtype=str)
xdats=pd.DataFrame(columns=gxdatSgn,dtype=str)

gidsFN=''
gidsNum=len(gids.index)
xdatsNum=len(xdats.index)
#
xbars=None
xnday_down=0

#----------class.fbt

class zTopFoolball(object):
    ''' 
    设置TopFoolball项目的各个全局参数
    尽量做到all in one

    '''

    def __init__(self):  
        #----rss.dir
        
        #
        self.tim0Str_gid='2010-01-01'
        self.tim0_gid=arrow.get(self.tim0Str_gid)
        
        #
        self.gid_tim0str,self.gid_tim9str='',''
        self.gid_nday,self.gid_nday_tim9=0,0
        #
        self.tim0,self.tim9,self.tim_now=None,None,None
        self.tim0Str,self.tim9Str,self.timStr_now='','',''
        #
        
        self.kgid=''
        self.kcid=''
        self.ktimStr=''
        #
        #----pool.1day
        self.poolInx=[]
        self.poolDay=pd.DataFrame(columns=poolSgn)
        #----pool.all
        self.poolTrd=pd.DataFrame(columns=poolSgn)
        self.poolRet=pd.DataFrame(columns=retSgn)
        self.poolTrdFN,self.poolRetFN='',''
        #
        self.bars=None
        self.gid10=None
        self.xdat10=None
        
        #
        #--backtest.var
        self.funPre,self.funSta=None,None
        self.preVars,self.staVars=[],[]
        #--backtest.ai.var
        #
        self.ai_mxFN0=''
        self.ai_mx_sgn_lst=[]
        self.ai_xlst=[]
        self.ai_ysgn=''
        self.ai_xdat,self.ai_xdat=None,None
        
        #
        #
        
        #
        #--ret.var
        self.ret_nday,self.ret_nWin=0,0
        self.ret_nplay,self.ret_nplayWin=0,0
        
        self.ret_msum=0
        
        

#----------zTopFoolball.init.obj
        

    