# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import os, re
import pexpect
import shlex, subprocess
from django.contrib.auth.decorators import login_required
from time import sleep

def get_isp():
    p = os.popen('ifconfig tun0')
    output = p.readlines()[1]
    ip = re.findall('inet (?P<ip>.*) -->', output)[0]
    isp = u'не определён'
    if re.findall('^10.', ip):  # GCN '^83.'
        isp = u'GCN'
    elif re.findall('^212.15.', ip):    # DSL
        isp = u'DSL'
    
    return isp
    
@login_required
def index(request):
    return render_to_response('index.html',
                        {'isp': get_isp()},
                        context_instance=RequestContext(request))
    

@login_required
def shutdown(request):
    #child = pexpect.spawn('sudo shutdown -r 1000')
    return render_to_response('shutdown.html',
                        {},
                        context_instance=RequestContext(request))


@login_required
def switch_isp(request):
    if 'isp' in request.REQUEST:
        target = request.REQUEST['isp']
        if target in ['gcn', 'dsl']:
            pexpect.spawn('sudo killall -9 ppp')
            sleep(1)
            pexpect.spawn('sudo /usr/sbin/ppp -quiet -ddial -nat %s' % target)
            return render_to_response('switch_isp.html',
                        {'isp': target},
                        context_instance=RequestContext(request))
    
    return HttpResponseRedirect('/')
