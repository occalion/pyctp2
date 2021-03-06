#-*- coding: utf-8 -*-

import operator

from collections import (
        deque,
    )


from base import (
        BaseObject,
        indicator,
        TICK,
    )

from utils import (
        fcustom,
    )

XBASE = 100  #整数运算的放大倍数
YBASE = XBASE * XBASE #

###############
# 基本序列运算
#
###############

@indicator
def OPER1(source,oper,_ts=None):
    '''
        单参数序列运算
    '''
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ss = []

    for i in range(len(_ts.ss),len(source)):
        #print 'new data:',source[i]
        _ts.ss.append(oper(source[i]))

    return _ts.ss

'''
    不同的operator.xxx, 使OPER1下缓存的key不同，不会导致混淆
'''
NEG = fcustom(OPER1,oper=operator.neg)
ABS = fcustom(OPER1,oper=operator.abs)
NOT = fcustom(OPER1,oper=operator.not_)

@indicator
def OPER2(source1,source2,oper,_ts=None):
    '''
        双参数序列运算
    '''
    assert len(source1) == len(source2),'len(source1) != len(source2)'
    if not _ts.initialized:
        _ts.initialized = True
        #print 'new oper2 ss'
        _ts.ss = []

    for i in range(len(_ts.ss),len(source1)):
        #print 'new data:',source1[i],source2[i]
        _ts.ss.append(oper(source1[i],source2[i]))

    return _ts.ss

ADD = fcustom(OPER2,oper=operator.add)
SUB = fcustom(OPER2,oper=operator.sub)
MUL = fcustom(OPER2,oper=operator.mul)
#AND = fcustom(OPER2,oper=operator.and_)    #这个是位操作
#OR = fcustom(OPER2,oper=operator.or_)      #这个是位操作
#XOR = fcustom(OPER2,oper=operator.xor)     #这个是位操作
LT = fcustom(OPER2,oper=operator.lt) 
LE = fcustom(OPER2,oper=operator.le) 
EQ = fcustom(OPER2,oper=operator.eq) 
GT = fcustom(OPER2,oper=operator.gt) 
GE = fcustom(OPER2,oper=operator.ge) 

@indicator
def OPER21(source1,vs,oper,_ts=None):
    '''
        双参数运算，第一个为序列，第二个为数值
    '''
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ss = []

    for i in range(len(_ts.ss),len(source1)):
        #print 'new data:',source1[i]
        _ts.ss.append(oper(source1[i],vs))

    return _ts.ss

ADD1 = fcustom(OPER21,oper=operator.add)
SUB1 = fcustom(OPER21,oper=operator.sub)
MUL1 = fcustom(OPER21,oper=operator.mul)
#AND1 = fcustom(OPER21,oper=operator.and_)  #这个是位操作
#OR1 = fcustom(OPER21,oper=operator.or_)    #这个是位操作
#XOR1 = fcustom(OPER21,oper=operator.xor)   #这个是位操作
LT1 = fcustom(OPER21,oper=operator.lt) 
LE1 = fcustom(OPER21,oper=operator.le) 
EQ1 = fcustom(OPER21,oper=operator.eq) 
GT1 = fcustom(OPER21,oper=operator.gt) 
GE1 = fcustom(OPER21,oper=operator.ge) 

@indicator
def AND(source1,source2,_ts=None):
    '''
        双序列参数AND运算
    '''
    assert len(source1) == len(source2),'len(source1) != len(source2)'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ss = []

    for i in range(len(_ts.ss),len(source1)):
        #print 'new data:',source1[i],source2[i]
        _ts.ss.append((source1[i] and source2[i])!=0)

    return _ts.ss


@indicator
def GAND(_ts=None,*args):
    assert len(args)>0,'GAND params number less than 1'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ga = []

    for i in range(len(_ts.ga),len(args[0])):
        rv = all([vs[i] for vs in args])
        _ts.ga.append(rv!=0)
        
    return _ts.ga

@indicator
def GOR(_ts=None,*args):
    assert len(args)>0,'GOR params number less than 1'
    #print 'ts=%s,args=%s' % (_ts,args)
    if not _ts.initialized:
        _ts.initialized = True
        _ts.gor = []

    for i in range(len(_ts.gor),len(args[0])):
        rv = any([vs[i] for vs in args])
        _ts.gor.append(rv!=0)
        
    return _ts.gor

#GAND = fcustom(GOPER,oper=all) #有可变参数时，就不能再有_ts之外的参数用fcustom指定默认值
#GOR = fcustom(GOPER,oper=any)  #有可变参数时，就不能再有_ts之外的参数用fcustom指定默认值


@indicator
def DIV(source1,source2,_ts=None):
    '''
        序列除法
    '''
    assert len(source1) == len(source2),'len(source1) != len(source2)'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ss = []

    for i in range(len(_ts.ss),len(source1)):
        #print 'new data:',source1[i],source2[i]
        r = (source1[i]+source2[i]//2)//source2[i] if source2[i] != 0 else source1[i]*1000
        _ts.ss.append(r)

    return _ts.ss

@indicator
def DIV1(source1,vs,_ts=None):
    '''
        序列除常数
    '''
    assert vs!=0,'divisor vs == 0'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ss = []

    for i in range(len(_ts.ss),len(source1)):
        #print 'new data:',source1[i]
        _ts.ss.append((source1[i]+vs//2)//vs)

    return _ts.ss


############
# 常用指标
#
############


@indicator
def ACCUMULATE(source,_ts=None):
    '''
        累加
    '''
    if not _ts.initialized:
        _ts.initialized = True
        _ts.sa = []

    ss = _ts.sa[-1] if _ts.sa else 0
    for i in range(len(_ts.sa),len(source)):
        ss += source[i]
        _ts.sa.append(ss)
    #print id(_ts),id(source),source,_ts.sa
    return _ts.sa

NSUM = ACCUMULATE

@indicator
def MSUM(source,mlen,_ts=None):
    '''
        移动求和
    '''
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ms = []

    ss = ACCUMULATE(source)
    for i in range(len(_ts.ms),len(source)):
        v = ss[i] - ss[i-mlen] if i>=mlen else ss[i]
        _ts.ms.append(v)
    return _ts.ms


@indicator
def MA(source,mlen,_ts=None):
    '''
        移动平均. 使用MSUM
        使用方式:
        rev = MA(source,13) #返回source的13期移动平均
        当序列中元素个数<mlen时，结果序列为到该元素为止的所有元素值的平均
    '''
    assert mlen>0,u'mlen should > 0'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.ma = []

    ms = MSUM(source,mlen)
    for i in range(len(_ts.ma),len(source)):
        #当累计个数<nlen时，求其平均值，而不是累计值/mlen
        rlen = mlen if i>=mlen else i+1
        _ts.ma.append((ms[i]+rlen//2)//rlen) 
    return _ts.ma


@indicator
def MA_2(source,mlen,_ts=None):
    '''
        移动平均. 直接计
        使用方式:
        rev = MA(source,13) #返回source的13期移动平均
        当序列中元素个数<mlen时，结果序列为到该元素为止的所有元素值的平均
    '''
    assert mlen>0,u'mlen should > 0'
    if not _ts.initialized:
        _ts.initialized = True
        _ts.sa = [0]*mlen   #哨兵
        _ts.ma = []

    slen = len(_ts.ma)
    ss = _ts.sa[-1]
    for i in range(slen,len(source)):
        ss += source[i]
        _ts.sa.append(ss)
        #print ss,_ts.sa[i-mlen]
        #当累计个数<nlen时，求其平均值，而不是累计值/mlen
        rlen = mlen if mlen < i+1 else i+1
        _ts.ma.append((ss-_ts.sa[-rlen-1]+rlen//2)//rlen) 
    #print _ts.sa
    return _ts.ma

@indicator
def NMA(source,_ts=None):
    '''
        总平均
        使用方式:
        rev = MA(source) #返回source的当期及之前的平均值
    '''
    if not _ts.initialized:
        _ts.initialized = True
        _ts.sa = [0]   #哨兵
        _ts.nma = []
        #print 'initial NMA'

    slen = len(_ts.nma)
    ss = _ts.sa[-1]
    for i in range(slen,len(source)):
        ss += source[i]
        _ts.sa.append(ss)
        #print ss,_ts.sa[-1]
        _ts.nma.append((ss+(i+1)//2)//(i+1)) 
    #print _ts.sa
    return _ts.nma


@indicator
def CEXPMA(source,mlen,_ts=None):
    assert mlen>0,u'mlen should > 0'
    if len(source) == 0:#不计算空序列，直接返回
        return []

    if not _ts.initialized:
        _ts.initialized = True
        #print 'new cexpma ema'
        _ts.ema = [source[0]]   #哨兵元素是source[0]，确保计算得到的值在<mlen元素的情况下也正确

    cur = _ts.ema[-1]
    for i in range(len(_ts.ema),len(source)):
        cur = (source[i]*2 + cur*(mlen-1) + (mlen+1)//2)//(mlen+1)
        _ts.ema.append(cur)
    return _ts.ema

EMA = CEXPMA

@indicator
def MACD(source,ifast=12,islow=26,idiff=9,_ts=None):
    if not _ts.initialized:
        _ts.initialized = True
        _ts.diff = []
        _ts.dea = []

    src = MUL1(source,FBASE)
    sfast = EMA(src,ifast)
    sslow = EMA(src,islow)
    _ts.diff = SUB(sfast,sslow)
    _ts.dea = EMA(_ts.diff,idiff)
    return _ts

@indicator
def TR(sclose,shigh,slow,_ts=None):
    if len(sclose) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        _ts.tr = [(shigh[0]-slow[0]) * XBASE]

    for i in range(len(_ts.tr),len(sclose)):
        #c,h,l = sclose[slen-1],shigh[slen],sclose[slen]
        hh = shigh[i] if shigh[i] > sclose[i-1] else sclose[i-1]
        ll = slow[i] if slow[i] < sclose[i-1] else sclose[i-1]
        _ts.tr.append((hh-ll)*XBASE)
    return _ts.tr

@indicator
def ATR(sclose,shigh,slow,length=20,_ts=None):
    ltr = TR(sclose,shigh,slow)
    return CEXPMA(ltr,length)


@indicator
def XATR(sclose,shigh,slow,length=20,_ts=None):
    latr = ATR(sclose,shigh,slow,length)
    return DIV(MUL1(latr,YBASE),sclose)


@indicator
def STREND(source,_ts=None):
    ''' 简单累积趋势2
        与strend相比，上升过程中，平也当作上,下降中平作下
        若当前趋势为上升或0，trend值为n>0
        则新trend值为：
            n+1 当前值 >= pre
            -1  当前值 < pre
        若当前趋势为下降，trend值为n(负数)
        则下一trend值为：
            n-1 当前值 <= pre
            1   当前值 > pre
        0为初始趋势(缺少判断时)
    '''
    if len(source) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        _ts.sd = [0]    #第一个是无趋势

    slen = len(_ts.sd)
    scur = _ts.sd[-1]
    vpre = source[slen-1]
    for i in range(slen,len(source)):
        vcur = source[i]
        if vcur > vpre:
            scur = scur + 1 if scur > 0 else 1
        elif vcur < vpre:
            scur = scur - 1 if scur < 0 else -1
        else: #curv == pre_v
            scur = scur + 1 if scur >= 0 else scur-1 #最初为0时，也算上升
        _ts.sd.append(scur)
        vpre = vcur
    return _ts.sd
 

#TMAX,TMIN,UCROSS,DCROSS
@indicator
def TMM(source,covered,vmm,fcmp,fgroup,_ts=None):
    ''' 
        vmm: 比较用的极值
        fcmp: 比较函数
        fgroup:整体比较函数

        cover=0时，返回的是截止到当前元素的最值(cover<0也如此)
    '''
    assert covered >=0, 'TMM: cover <0'
    if len(source) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        #print 'new tmm'
        _ts.tmm = []    #第一个是无趋势
        _ts.buffer = None

    slen = len(source)
    pre_len = slen if slen <= covered else covered
    cmm = _ts.tmm[-1] if _ts.tmm else vmm
    for i in range(len(_ts.tmm),pre_len):
        if fcmp(source[i],cmm):
            cmm = source[i]
        _ts.tmm.append(cmm)
    if slen <= covered:
        return _ts.tmm
    tlen = len(_ts.tmm)
    if _ts.buffer:
        buffer = _ts.buffer
    else:
        buffer = _ts.buffer = deque(source[tlen-covered:tlen])  
    #print 'in tmm:tlen=%s,len(source)=%s' % (tlen,len(source))
    for i in range(tlen,len(source)):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        if fcmp(v,cmm):
            cmm = v
        if cmm == vquit and v != cmm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            #cmm = fgroup(source[i-covered+1:i+1])
            cmm = fgroup(buffer)
        _ts.tmm.append(cmm)
    return _ts.tmm

TMAX = fcustom(TMM,vmm=-99999999,fcmp=operator.gt,fgroup=max)
TMIN = fcustom(TMM,vmm=99999999,fcmp=operator.lt,fgroup=min)

@indicator
def NMM(source,vmm,fcmp,_ts=None):
    '''
        从index0算起的极值.
        相当于covered取最大值时的TMM
    '''
    if len(source) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        #print 'new nmm'
        _ts.nmm = []    #第一个是无趋势

    slen = len(source)
    cmm = _ts.nmm[-1] if _ts.nmm else vmm
    for i in range(len(_ts.nmm),len(source)):
        if fcmp(source[i],cmm):
            cmm = source[i]
        _ts.nmm.append(cmm)
    return _ts.nmm
NMAX = fcustom(NMM,vmm=-99999999,fcmp=operator.gt)
NMIN = fcustom(NMM,vmm=99999999,fcmp=operator.lt)


@indicator
def CROSS(source1,source2,rcmp,_ts=None):
    '''
        source2去交叉source1
        rcmp为判断已交叉状态的函数
        返回值中,0为未×,1为×
    '''
    if len(source1) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        _ts.crs = [1 if rcmp(source2[0],source1[0]) else 0]   #第一个取决于状态，如果为已×，则为1

    ps = _ts.crs[-1]
    for i in range(len(_ts.crs),len(source1)):
        cs = rcmp(source2[i],source1[i])
        _ts.crs.append(1 if not ps and cs else 0)
        ps = cs
    return _ts.crs

UPCROSS = fcustom(CROSS,rcmp = operator.gt) #追击-平-平-超越，以及超越-平-超越均算×
DOWNCROSS = fcustom(CROSS,rcmp = operator.lt) #追击-平-平-超越，以及超越-平-超越均算×

@indicator
def NCROSS(source,target,rcmp,_ts=None):
    '''
        source去交叉target, target为数字
        rcmp为判断已交叉状态的函数
        返回值中,0为未×,1为×
    '''
    if len(source) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        _ts.crs = [1 if rcmp(source[0],target) else 0]   #第一个取决于状态，如果为已×，则为1

    ps = _ts.crs[-1]
    for i in range(len(_ts.crs),len(source)):
        cs = rcmp(source[i],target)
        _ts.crs.append(1 if not ps and cs else 0)
        ps = cs
    return _ts.crs

NUPCROSS = fcustom(NCROSS,rcmp = operator.gt) #追击-平-平-超越，以及超越-平-超越均算×
NDOWNCROSS = fcustom(NCROSS,rcmp = operator.lt) #追击-平-平-超越，以及超越-平-超越均算×


@indicator
def REF(source,offset=1,_ts=None):
    '''
        取得偏移为offset的序列
        前offset部分用第一元素填充
        如果仅用于比较,不建议用这个函数,而直接用[-1]下标比较
        只有在偏移CROSS时才有意义
    '''
    if len(source) == 0:
        return []

    if not _ts.initialized:
        _ts.initialized = True
        _ts.ref = [source[0]]
        #print 'initialize REF'
    
    for i in range(len(_ts.ref),offset if offset <= len(source) else len(source)):
        _ts.ref.append(source[0])

    for i in range(len(_ts.ref),len(source)):
        _ts.ref.append(source[i-offset])

    return _ts.ref

####分钟切换
time2min = lambda t:t//100000

NullMinute = BaseObject(sopen=[],sclose=[],shigh=[],slow=[],svol=[],sholding=[],sdate=[],stime=[],modified=False)

@indicator
def MINUTE_1(ticks,pre_min1=None,_ts=None):
    '''
        分钟切分, 以ticks为参数
        _ts用于暂存。同时可用于接续历史数据
        如果pre_min1不为空，调用者需保证ticks[0].min1 > pre_min1.stime
    '''

    if len(ticks) == 0:
        return NullMinute

    if not _ts.initialized:
        _ts.initialized = True
        if pre_min1 == None:    #不接续
            _ts.sopen = []
            _ts.sclose = []
            _ts.shigh = []
            _ts.slow = []
            _ts.svol = []
            _ts.sholding=[]
            _ts.sdate = []
            _ts.stime = []
        else:
            _ts.sopen = pre_min1.sopen
            _ts.sclose = pre_min1.sclose
            _ts.shigh = pre_min1.shigh
            _ts.slow = pre_min1.slow
            _ts.svol = pre_min1.svol
            _ts.sholding=pre_min1.sholding
            _ts.sdate = pre_min1.sdate
            _ts.stime = pre_min1.stime
        _ts.cur = BaseObject(vopen = ticks[0].price,    
                             vclose = ticks[0].price,   
                             vhigh=ticks[0].price,      
                             vlow=ticks[0].price,       
                             open_dvol=ticks[0].dvolume,#存在初始误差
                             close_dvol=ticks[0].dvolume,
                             holding = ticks[0].holding,
                             xtime=ticks[0].min1,    #当日第一min1
                             xdate=ticks[0].date,
                        )  #这里对dvol的处理,使得中断恢复也必须从当日最开始开始,否则所有前述成交量被归结到第一tick
        _ts.ilast = 0
        _ts.modified = False    #上周期完成标志

    scur = _ts.cur
    for i in range(_ts.ilast,len(ticks)):
        tcur = ticks[i]
        #print tcur.min1,scur.xtime
        if tcur.min1 > scur.xtime or (tcur.min1 == 0 and scur.xtime > 0) or (tcur.date > scur.xdate and scur.xtime > 0):  #tcur.min1 = 0, 分钟切换用,要求其它字段均为0
            if scur.xtime > 0:  #前一分钟不是切换标志
                _ts.sopen.append(scur.vopen)
                _ts.sclose.append(scur.vclose)
                _ts.shigh.append(scur.vhigh)
                _ts.slow.append(scur.vlow)
                _ts.svol.append(scur.close_dvol - scur.open_dvol)
                _ts.sholding.append(scur.holding)
                _ts.sdate.append(scur.xdate)
                _ts.stime.append(scur.xtime)
            scur.vopen = scur.vclose = scur.vhigh = scur.vlow = tcur.price
            scur.open_dvol = scur.close_dvol
            scur.close_dvol = tcur.dvolume
            scur.dvol = tcur.dvolume
            scur.holding = tcur.holding
            scur.xdate = tcur.date
            scur.xtime = tcur.min1
            _ts.modified = True
        else:   #未切换
            scur.vclose = tcur.price
            scur.close_dvol = tcur.dvolume
            scur.holding = tcur.holding
            #print scur.xtime,'close:',scur.vclose
            if tcur.price > scur.vhigh:
                scur.vhigh = tcur.price
            elif tcur.price < scur.vlow:
                scur.vlow = tcur.price
            _ts.modified = False

    _ts.ilast = len(ticks)
    return _ts

@indicator
def MINUTE(dates,times,prices,dvols,holdings,pre_min1=None,_ts=None):
    '''
        分钟切分, 参数不同
        _ts用于暂存。同时可用于接续历史数据
        如果pre_min1不为空，调用者需保证ticks[0].min1 > pre_min1.stime
    '''

    if len(prices) == 0:
        return NullMinute

    if not _ts.initialized:
        _ts.initialized = True
        if pre_min1 == None:    #不接续
            _ts.sopen = []
            _ts.sclose = []
            _ts.shigh = []
            _ts.slow = []
            _ts.svol = []
            _ts.sholding=[]
            _ts.sdate = []
            _ts.stime = []
        else:
            _ts.sopen = pre_min1.sopen
            _ts.sclose = pre_min1.sclose
            _ts.shigh = pre_min1.shigh
            _ts.slow = pre_min1.slow
            _ts.svol = pre_min1.svol
            _ts.sholding=pre_min1.sholding
            _ts.sdate = pre_min1.sdate
            _ts.stime = pre_min1.stime
        _ts.cur = BaseObject(vopen = prices[0],
                             vclose = prices[0],
                             vhigh=prices[0],
                             vlow=prices[0],
                             open_dvol=dvols[0],#存在初始误差
                             close_dvol=dvols[0],
                             holding = holdings[0],
                             xtime=time2min(times[0]),    #启动后第一min1
                             xdate=dates[0],
                        )  #这里对dvol的处理,使得中断恢复也必须从当日最开始开始,否则所有前述成交量被归结到第一tick
        _ts.ilast = 0
        _ts.modified = False    #上周期完成标志

    _ts.modified = False    #上周期完成标志
    scur = _ts.cur
    for i in range(_ts.ilast,len(prices)):
        tmin1 = time2min(times[i])
        if tmin1 > scur.xtime or (tmin1 == 0 and scur.xtime > 0) or (dates[i]>scur.xdate and scur.xtime > 0):  #tcur.min1 = 0, 分钟切换用,要求其它字段均为0
            if scur.xtime > 0:  #前一分钟不是切换标志
                _ts.sopen.append(scur.vopen)
                _ts.sclose.append(scur.vclose)
                _ts.shigh.append(scur.vhigh)
                _ts.slow.append(scur.vlow)
                _ts.svol.append(scur.close_dvol - scur.open_dvol)
                _ts.sholding.append(scur.holding)
                _ts.sdate.append(scur.xdate)
                _ts.stime.append(scur.xtime)
            scur.vopen = scur.vclose = scur.vhigh = scur.vlow = prices[i]
            scur.open_dvol = scur.close_dvol
            scur.close_dvol = dvols[i]
            scur.dvol = dvols[i]
            scur.holding = holdings[i]
            scur.xdate = dates[i]
            scur.xtime = tmin1
            _ts.modified = True
        else:   #未切换
            scur.vclose = prices[i]
            scur.close_dvol = dvols[i]
            scur.holding = holdings[i]
            #print tmin1,'close:',scur.vclose
            if prices[i] > scur.vhigh:
                scur.vhigh = prices[i]
            elif prices[i] < scur.vlow:
                scur.vlow = prices[i]

    _ts.ilast = len(prices)
    return _ts

