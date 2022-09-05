import secs
import re
import os,sys
import configparser
str = ''
def repl_func(matched):
    if matched:
        text = matched.group(0)
        text = text.split("<A ")[1]
        text = text[0:len(text)-1]
        
        return '<A "'+text+'">'

def recv_primary_msg(primary, comm):

            strm = primary.strm
            func = primary.func
            wbit = primary.wbit
            
            def _sxf0(x):
                comm.reply(primary, x, 0, False)

            try:
                if strm == 1:

                    if func == 13:
                        if wbit:
                            comm.gem.s1f14(primary, secs.COMMACK.OK)

                    elif func == 15:
                        if wbit:
                            comm.gem.s1f16(primary)

                    elif func == 17:
                        if wbit:
                            comm.gem.s1f18(primary, secs.ONLACK.OK)

                    else:
                        if wbit:
                            _sxf0(strm)
                        comm.gem.s9f5(primary)


                elif strm == 2:

                    if func == 31:
                        if wbit:
                            comm.gem.s2f32(primary, secs.TIACK.OK)

                    else:
                        if wbit:
                            _sxf0(strm)
                        comm.get.s9f5(primary)

                else:
                    if wbit:
                        _sxf0(strm)
                    comm.get.s9f3(primary)

            except Exception as e:
                raise e

if __name__ == '__main__':
    os.chdir(sys.path[0])
    config = configparser.ConfigParser() # 类实例化
    config.read("EQPDEF.ini")
    print("*******************Simulator Start ***********************")

    passive = secs.HsmsSsPassiveCommunicator(
        ip_address='127.0.0.1',
        port=5000,
        session_id=10,
        is_equip=True,
        timeout_t3=45.0,
        timeout_t6=5.0,
        timeout_t7=10.0,
        timeout_t8=5.0,
        gem_mdln='MDLN-A',
        gem_softrev='000001',
        gem_clock_type=secs.ClockType.A16,
        name='equip-passive-comm')

    passive.open()
    passive.add_recv_primary_msg_listener(recv_primary_msg)

    str = ''
    msgs = []
    with open("TDTHK01.sml", mode='r') as f:
        while True:
            line = f.readline()
            if line == '': 
                msgs.append(str)
                str = ''
                break
            if line == '\n':
                msgs.append(str)
                str = ''
            else:
                str += line

    # sml_str = sml.replace('\n', ' ').strip()
    # s1 = sml_str.split(".")
    # _SML_PATTERN = '[Ss]([0-9]{1,3})[Ff]([0-9]{1,3}):\\s*([Ww]?)\\s*((<.*>)?)\\s*\\.$'
    # _SML_PROG = re.compile(_SML_PATTERN)
    # m = _SML_PROG.search(sml_str)
    # print(m.group(0))
    # m = re.findall(_SML_PATTERN,sml_str)
    # print(s1)
    CarrierStateTransEvt_2_PORTX = config['CEID_TABLE']['CarrierStateTransEvt_2_PORTX'].split(',')[0]
    CarrierStateTransEvt_3_PORTX = config['CEID_TABLE']['CarrierStateTransEvt_3_PORTX'].split(',')[0]



    


    a = input("input:请输入结束")

    for msg in msgs:
        msg = re.sub(r'\*.*','',msg)
        print(msg)
        msg = re.sub(r'\[.\]\s[a-zA-Z0-9]*\s','',msg)
        print(msg)
        msg = re.sub(r'<A\s[0-9a-zA-Z]*>',repl_func,msg)
        print(msg)   

        msg = msg.replace('\n', ' ').strip()
        msg = msg.replace('\t', ' ').strip()
        
        # msg = re.sub(r'\*.*','',msg)
        m = re.search(r'(<U4 2012>)',msg)
        if m != None:
            m = re.search(r'S6F11:',msg)
            end = m.end(0)
            msg = "S6F11 W"+msg[end:-1]+'>.'
            try:
                passive.send_sml(msg)
            except Exception as e :
                print(e)
                # raise Secs2BodySmlParseError(str(e))
            
            print(msg)

    
