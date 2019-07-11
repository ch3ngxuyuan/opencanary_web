#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
  Author: pirogue 
  Purpose: 日志表操作
  Site: http://pirogue.org 
  Created: 2018-08-03 17:32:54
"""

from dbs.initdb import DBSession
from dbs.models.HoneypotLog import OpencanaryLog
from dbs.models.Whiteip import Whiteip
from sqlalchemy import desc, asc, extract, func, distinct, and_,or_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.sql import text

class LogOp:
    """增删改查"""

    def __init__(self):
        self.session = DBSession

    def insert(self, dst_host, dst_port, honeycred, local_time, hostname, password, path, skin,\
             useragent, username, session, localversion, remoteversion, df, idid, inin, lenlen, mac, outout,\
             prec, proto, res, syn, tos, ttl, urgp, window, logtype, node_id, src_host, src_port, white, \
             repo, ntp_cmd, args, cmd, banner_id, data, function, vnc_client_response, vnc_password, \
             vnc_server_challenge, inputs, domain, headers_call_id, headers_content_length,headers_cseq, \
             headers_from, headers_to, headers_via, community_string, requests, urg, psh, fin, \
             appname, cltintname, database, language, servername, domainname):

        loginsert = OpencanaryLog(dst_host=dst_host, dst_port=dst_port, honeycred=honeycred, local_time=local_time,\
            hostname=hostname, password=password, path=path, skin=skin, useragent=useragent, username=username,\
            session=session, localversion=localversion, remoteversion=remoteversion, df=df, idid=idid, inin=inin,\
            lenlen=lenlen, mac=mac, outout=outout, prec=prec, proto=proto, res=res, syn=syn, tos=tos, ttl=ttl,\
            urgp=urgp, window=window, logtype=logtype, node_id=node_id, src_host=src_host, src_port=src_port, white=white,\
            # 扩表后的新加入库字段
            repo=repo, ntp_cmd=ntp_cmd, args=args, cmd=cmd, banner_id=banner_id, data=data, function=function, \
            vnc_client_response=vnc_client_response, vnc_password=vnc_password, vnc_server_challenge=vnc_server_challenge, \
            inputs=inputs, domain=domain, headers_call_id=headers_call_id, headers_content_length=headers_content_length, \
            headers_cseq=headers_cseq, headers_from=headers_from, headers_to=headers_to, headers_via=headers_via, \
            community_string=community_string, requests=requests, urg=urg, psh=psh, fin=fin, \
            appname=appname, cltintname=cltintname, database=database, language=language, servername=servername, domainname=domainname)

        if loginsert:
            try:
                self.session.add(loginsert)
                self.session.commit()
                return True
            except InvalidRequestError:
                self.session.rollback()
            except Exception as e:
                print(e)
            finally:
                self.session.close()
        else:
            return False

    # 查询日志表攻击列表数据
    def page_select_attack(self, page_index, src_host,src_port,logtype,node_id,dst_host,dst_port):
        try:
            page_size = 10
            # num = 10*int(page) - 10
            where = "white = 2"
            if src_host:
                where += ' and src_host="' + str(src_host) + '"'
            if src_port:
                where += " and src_port=" + src_port
            if logtype:
                if logtype=='18001':
                    where += ' and logtype in("18001","18002","18003","18004","18005") '
                else:
                    where += ' and logtype="' + str(logtype) + '"'
            if node_id:
                where += ' and node_id="' + str(node_id) + '"'
            if dst_host:
                where += ' and dst_host="' + str(dst_host) + '"'
            if dst_port:
                where += " and dst_port=" + dst_port
            logselect = self.session.query(OpencanaryLog).filter(
                text(where)).order_by(
                    desc(OpencanaryLog.local_time),
                    OpencanaryLog.id).limit(page_size).offset(
                        (page_index - 1) * page_size)
            return logselect
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 查询日志表白名单数据
    def page_select_white(self, page_index):
        try:
            page_size = 10
            # num = 10*int(page) - 10
            logselect = self.session.query(OpencanaryLog).filter(
                OpencanaryLog.white == 1).order_by(
                    desc(OpencanaryLog.local_time),
                    OpencanaryLog.id).limit(page_size).offset(
                        (page_index - 1) * page_size)
            return logselect
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 查询当年每月攻击数量
    def attack_select_num(self, months):
        try:
            attack_num = self.session.query(
                extract('month', OpencanaryLog.local_time).label('month'),
                func.count('*').label('count')).filter(
                    extract('year', OpencanaryLog.local_time) == months,
                    OpencanaryLog.white == 2).group_by('month').all()
            return attack_num
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 查询当年每月白名单内攻击数量
    def white_select_num(self, months):
        try:
            white_num = self.session.query(
                extract('month', OpencanaryLog.local_time).label('month'),
                func.count('*').label('count')).filter(
                    extract('year', OpencanaryLog.local_time) == months,
                    OpencanaryLog.white == 1).group_by('month').all()
            return white_num
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 查询各类攻击数量
    def pie_select_num(self, years):
        try:
            pie_num = self.session.query(
                func.count(OpencanaryLog.logtype),
                OpencanaryLog.logtype).group_by(OpencanaryLog.logtype).filter(
                    extract('year', OpencanaryLog.local_time) == years,
                    OpencanaryLog.white == 2).all()
            return pie_num
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 查询攻击数据总量
    def select_attack_total(self,src_host,src_port,logtype,node_id,dst_host,dst_port):
        try:
            where = "white = 2"
            if src_host:
                where += ' and src_host="' + str(src_host) + '"'
            if src_port:
                where += " and src_port=" + src_port
            if logtype:
                if logtype=='18001':
                    where += ' and logtype in("18001","18002","18003","18004","18005") '
                else:
                    where += ' and logtype="' + str(logtype) + '"'
            if node_id:
                where += ' and node_id="' + str(node_id) + '"'
            if dst_host:
                where += ' and dst_host="' + str(dst_host) + '"'
            if dst_port:
                where += " and dst_port=" + dst_port
            total_attack = self.session.query(
                func.count(OpencanaryLog.id)).filter(
                    text(where)).scalar()
            return total_attack
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()
            
    # 查询过滤列表总量
    def select_filter_total(self):
        try:
            total_filter = self.session.query(
                func.count(OpencanaryLog.id)).filter(
                    OpencanaryLog.white == 1).scalar()
            return total_filter
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()