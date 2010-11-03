# Copyright (C) 2009 Raul Jimenez
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

from nose.tools import ok_, eq_, assert_raises

import node
import logging, logging_conf

import test_const as tc
import bencode
import message as m
import message_tools as mt

logging_conf.testing_setup(__name__)
logger = logging.getLogger('dht')


class TestMsg:

    def setup(self):
        pass
        
    def test_matching_tid(self):
        # It _only_ matches the first byte)
        ok_(m.matching_tid('aaa', 'aaa'))
        ok_(m.matching_tid('axa', 'a1a'))
        ok_(m.matching_tid('aQWEREWTWETWTWETWETEWT', 'a'))
        ok_(not m.matching_tid('a', 'b'))
        ok_(not m.matching_tid('aZZ', 'bZZ'))
        
    def test_ping(self):
        #client
        outgoing_query = m.OutgoingPingQuery(tc.CLIENT_ID)
        data = outgoing_query.encode(tc.TID) # query_manager would do it
        #server
        incoming_query = m.IncomingMsg(data)
        assert incoming_query.type is m.QUERY
        outgoing_response = m.OutgoingPingResponse(tc.SERVER_ID)
        data = outgoing_response.encode(incoming_query.tid)
        #client
        incoming_response = m.IncomingMsg(data)
        assert incoming_response.type is m.RESPONSE
        incoming_response.sanitize_response(outgoing_query.query)
    '''
    def _test_ping_error(self):
        outgoing_query = m.OutgoingPingQuery(tc.CLIENT_ID)
        #outgoing_query.my_id = CLIENT_ID
        #outgoing_query.tid = tc.TID
        # TID and ARGS ID are None
        assert_raises(m.MsgError, outgoing_query.encode)
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")

        outgoing_query = m.OutgoingPingQuery()
        outgoing_query.my_id = tc.CLIENT_ID
        #outgoing_query.tid = tc.TID
        assert_raises(m.MsgError, outgoing_query.encode)
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")

        outgoing_query = m.OutgoingPingQuery()
        #outgoing_query.my_id = tc.CLIENT_ID
        outgoing_query.tid = tc.TID
        assert_raises(m.MsgError, outgoing_query.encode)
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")
        
        outgoing_query = m.OutgoingPingQuery()
        assert_raises(m.MsgError, outgoing_query.__setattr__, 'my_id', '')
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")
                
        outgoing_query = m.OutgoingPingQuery()
        outgoing_query.my_id = tc.CLIENT_ID
        outgoing_query.tid = 567
        data = outgoing_query.encode()
        assert_raises(m.MsgError, m.decode, data)
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")

        outgoing_query = m.OutgoingPingQuery()
        outgoing_query.my_id = tc.CLIENT_ID
        outgoing_query.tid = tc.TID
        data = outgoing_query.encode()
        data += 'this string ruins the bencoded msg'
        assert_raises(m.MsgError, m.decode, data)
        logger.error(
            "**IGNORE 2 ERROR LOGS** This exception was raised by a test")



        
        outgoing_response = m.OutgoingPingResponse(tc.TID, tc.SERVER_ID)
        outgoing_response.tid = None
        assert_raises(m.MsgError, outgoing_response.encode)
        logger.error(
            "**IGNORE ERROR LOGS** This exception was raised by a test")

    '''
    def test_find_node(self):
        #client
        outgoing_query = m.OutgoingFindNodeQuery(tc.CLIENT_ID, tc.NODE_ID)
        data = outgoing_query.encode(tc.TID)
        #server
        incoming_query = m.IncomingMsg(data)
        assert incoming_query.type is m.QUERY
        outgoing_response = m.OutgoingFindNodeResponse(tc.SERVER_ID,
                                                     tc.NODES)
        data = outgoing_response.encode(incoming_query.tid)
        #client
        incoming_response = m.IncomingMsg(data)
        eq_(incoming_response.type, m.RESPONSE)
        incoming_response.sanitize_response(outgoing_query.query)
        for n1, n2 in zip(tc.NODES, incoming_response.nodes2):
            eq_(n1, n2)


    def test_find_node_error(self):
        assert_raises(m.MsgError, m.OutgoingFindNodeResponse,
                      tc.CLIENT_ID, nodes=tc.NODES)
        assert_raises(m.MsgError, m.OutgoingFindNodeResponse,
                      tc.CLIENT_ID)

        
    def test_get_peers_nodes(self):
        #client
        outgoing_query = m.OutgoingGetPeersQuery(tc.CLIENT_ID, tc.INFO_HASH)
        data = outgoing_query.encode(tc.TID)
        #server
        incoming_query = m.IncomingMsg(data)
        assert incoming_query.type is m.QUERY
        outgoing_response = m.OutgoingGetPeersResponse(tc.SERVER_ID,
                                                     tc.TOKEN,
                                                     nodes2=tc.NODES)
        data = outgoing_response.encode(incoming_query.tid)
        #client
        incoming_response = m.IncomingMsg(data)
        assert incoming_response.type is m.RESPONSE
        incoming_response.sanitize_response(outgoing_query.query)
        for n1, n2 in zip(tc.NODES, incoming_response.nodes2):
            assert n1 == n2

    def test_get_peers_nodes_error(self):
        assert_raises(m.MsgError, m.OutgoingGetPeersResponse,
                      tc.CLIENT_ID, tc.TOKEN)
                        
    def test_get_peers_peers(self):
        #client
        outgoing_query = m.OutgoingGetPeersQuery(tc.CLIENT_ID, tc.INFO_HASH)
        data = outgoing_query.encode(tc.TID)
        #server
        incoming_query = m.IncomingMsg(data)
        assert incoming_query.type is m.QUERY
        outgoing_response = m.OutgoingGetPeersResponse(tc.SERVER_ID,
                                                     tc.TOKEN,
                                                     peers=tc.PEERS)
        data = outgoing_response.encode(incoming_query.tid)
        #client
        incoming_response = m.IncomingMsg(data)
        assert incoming_response.type is m.RESPONSE
        incoming_response.sanitize_response(outgoing_query.query)
        for p1, p2 in zip(tc.PEERS, incoming_response.peers):
            assert p1[0] == p2[0]
            assert p1[1] == p2[1]

    def test_get_peers_peers_error(self):
        assert 1

    def test_announce_peer(self):
        #client
        outgoing_query = m.OutgoingAnnouncePeerQuery(tc.CLIENT_ID,
                                                   tc.INFO_HASH,
                                                   tc.BT_PORT,
                                                   tc.TOKEN)
        outgoing_query.tid = tc.TID
        data = outgoing_query.encode(tc.TID)
        #server
        incoming_query = m.IncomingMsg(data)
        assert incoming_query.type is m.QUERY
        outgoing_response = m.OutgoingAnnouncePeerResponse(tc.SERVER_ID)
        data = outgoing_response.encode(incoming_query.tid)
        #client
        incoming_response = m.IncomingMsg(data)
        assert incoming_response.type is m.RESPONSE
        incoming_response.sanitize_response(outgoing_query.query)

    def test_announce_peer_error(self):
        assert 1
    '''
    def _test_error(self):
        outgoing_error_msg = m.OutgoingErrorMsg(tc.TID, m.GENERIC_E)
        data = outgoing_error_msg.encode()
        tid, msg_type, msg_dict = m.decode(data)
        incoming_error_msg = m.IncomingErrorMsg(msg_dict)
        logger.debug(incoming_error_msg.error)
        assert incoming_error_msg.error == m.GENERIC_E
    '''

def value_is_string(msg_d, k, valid_values=None):
    v = msg_d[k]
    ok_(isinstance(v, str))
    
        

class TestIncomingMsg:

    def setup(self):
        b_ping = m.OutgoingPingQuery(tc.CLIENT_ID).encode(tc.TID)
        self.msg_d = m.IncomingMsg(b_ping)._msg_dict

    def test_bad_bencode(self):
        assert_raises(m.MsgError, m.IncomingMsg, 'z')
        assert_raises(m.MsgError, m.IncomingMsg, '1:aa')
        assert_raises(m.MsgError, m.IncomingMsg, 'd')

    def test_not_a_dict(self):
        msgs = ([], 'a', 1)
        for msg in msgs:               
            assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(msg))

    def test_tid_error(self):
        # no TID
        del self.msg_d[m.TID] 
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        # invalid m.TID
        self.msg_d[m.TID] = 1
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        self.msg_d[m.TID] = []
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        self.msg_d[m.TID] = {}
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        
    def test_type_error(self):
        # no TYPE
        del self.msg_d[m.TYPE] 
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        # invalid m.TYPE
        self.msg_d[m.TYPE] = 1
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        self.msg_d[m.TYPE] = []
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        self.msg_d[m.TYPE] = {}
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))
        # unknown m.TYPE
        self.msg_d[m.TYPE] = 'z'
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.msg_d))

    def test_version_not_present(self):
        del self.msg_d[m.VERSION]
        m.IncomingMsg(bencode.encode(self.msg_d))

    def test_unknown_error(self):
        error_code = (999, "some weird error string")
        b_err = m.OutgoingErrorMsg(error_code).encode(tc.TID)
        
        logger.info(
            "TEST LOGGING ** IGNORE EXPECTED INFO ** Unknown error: %r",
            error_code)
        _ = m.IncomingMsg(b_err)


        
b_ping_q = m.OutgoingPingQuery(tc.CLIENT_ID).encode(tc.TID)
b_fn_q = m.OutgoingFindNodeQuery(tc.CLIENT_ID, tc.NODE_ID).encode(tc.TID)
b_gp_q = m.OutgoingGetPeersQuery(tc.CLIENT_ID, tc.INFO_HASH).encode(tc.TID)
b_ap_q = m.OutgoingAnnouncePeerQuery(tc.CLIENT_ID, tc.INFO_HASH,
                                 tc.BT_PORT,tc.TOKEN).encode(tc.TID)

class TestSanitizeQueryError:

    def setup(self):
        self.ping_d = m.IncomingMsg(b_ping_q)._msg_dict
        self.fn_d = m.IncomingMsg(b_fn_q)._msg_dict
        self.gp_d = m.IncomingMsg(b_gp_q)._msg_dict
        self.ap_d = m.IncomingMsg(b_ap_q)._msg_dict

    def test_weird_msg(self):
        self.ping_d[m.ARGS] = []
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.ARGS] = 1
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.ARGS] = 'ZZZZ'
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        
        
        
    def test_sender_id(self):
        # no sender_id
        del self.ping_d[m.ARGS][m.ID]
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        # bad ID
        self.ping_d[m.ARGS][m.ID] = 'a'
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.ARGS][m.ID] = 1
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.ARGS][m.ID] = []
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.ARGS][m.ID] = {}
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))

    def test_query(self): 
        # no m.QUERY
        del self.ping_d[m.QUERY]
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        # bad m.QUERY
        self.ping_d[m.QUERY] = 1
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.QUERY] = []
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        self.ping_d[m.QUERY] = {}
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ping_d))
        # unknown m.QUERY is not an error at this point
        # responder will process it and send an errror msg if necesary
        self.ping_d[m.QUERY] = 'a'
        m.IncomingMsg(bencode.encode(self.ping_d))

    def test_announce(self):
        # Port must be integer
        self.ap_d[m.ARGS][m.PORT] = 'a'
        assert_raises(m.MsgError, m.IncomingMsg, bencode.encode(self.ap_d))

        
b_ping_r = m.OutgoingPingResponse(tc.CLIENT_ID).encode(tc.TID)
b_fn2_r = m.OutgoingFindNodeResponse(tc.CLIENT_ID, nodes2=tc.NODES).encode(tc.TID)
b_gp_r = m.OutgoingGetPeersResponse(tc.CLIENT_ID, token=tc.TOKEN,
                                peers=tc.PEERS).encode(tc.TID)
b_ap_r = m.OutgoingAnnouncePeerResponse(tc.CLIENT_ID).encode(tc.TID)

class TestSanitizeResponseError:

    def setup(self):
        self.ping_r = m.IncomingMsg(b_ping_r)
        self.fn2_r = m.IncomingMsg(b_fn2_r)
        self.gp_r = m.IncomingMsg(b_gp_r)
        self.ap_r = m.IncomingMsg(b_ap_r)

    def test_nodes_not_implemented(self):
        assert_raises(m.MsgError, m.OutgoingFindNodeResponse, tc.CLIENT_ID,
                                        nodes=tc.NODES)
    def test_sanitize(self):
        self.ping_r.sanitize_response(m.PING)

        del self.fn2_r._msg_dict[m.RESPONSE][m.NODES2]
        # No NODES and no NODES2
        assert_raises(m.MsgError, self.fn2_r.sanitize_response, m.FIND_NODE)
        self.fn2_r._msg_dict[m.RESPONSE][m.NODES] = \
            mt.compact_nodes(tc.NODES)
        # Just NODES
        self.fn2_r.sanitize_response(m.FIND_NODE)
        self.fn2_r._msg_dict[m.RESPONSE][m.NODES2] = \
            mt.compact_nodes2(tc.NODES)
        # Both NODES and NODES2
        self.fn2_r.sanitize_response(m.FIND_NODE)

        # Both NODES and PEERS in response
        self.gp_r._msg_dict[m.RESPONSE][m.NODES] = \
            mt.compact_nodes(tc.NODES)
        self.gp_r.sanitize_response(m.GET_PEERS)
        # No NODES and no PEERS
        del self.gp_r._msg_dict[m.RESPONSE][m.NODES]
        del self.gp_r._msg_dict[m.RESPONSE][m.VALUES]
        assert_raises(m.MsgError, self.gp_r.sanitize_response, m.GET_PEERS)
        
        
class TestSanitizeErrorError:

    def test(self):
        msg_out = m.OutgoingErrorMsg(1).encode(tc.TID)
        assert_raises(m.MsgError, m.IncomingMsg, msg_out)
        # Unknown error doesn't raise m.MsgError
        msg_out = m.OutgoingErrorMsg((1,1)).encode(tc.TID)
        _ = m.IncomingMsg(msg_out)
    


        
class TestPrinting:
    
    def test_printing(self):
        out_msg = m.OutgoingPingQuery(tc.CLIENT_ID)
        in_msg = m.IncomingMsg(out_msg.encode(tc.TID))
        str(out_msg)
        repr(out_msg)
        repr(in_msg)
    
                  
