# encoding: utf-8
##
# This file is part of WhatWeb and may be subject to
# redistribution and commercial restrictions. Please see the WhatWeb
# web site for more information on licensing and terms of use.
# http://www.morningstarsecurity.com/research/whatweb
##
Plugin.define "wolfcms" do
    author "国光 <admin@sqlsec.com>" #20180901
    version "0.1"
    description "Wolf CMS是Wolf CMS团队开发的一套基于PHP的开源内容管理系统（CMS）。该系统提供用户界面、模板、用户管理和权限管理等功能。"
    website "http://www.wolfcms.org/"
    
    # Matches #
  matches [
      
        {:text=>'/public/themes/simple/images/favicon.ico'},
        {:text=>'http://www.wolfcms.org/'},
        {:text=>'/?articles/'},
        # url exists, i.e. returns HTTP status 200
        {:url=>"/wolf/index.html"},
        ]
        
            
    end
    
