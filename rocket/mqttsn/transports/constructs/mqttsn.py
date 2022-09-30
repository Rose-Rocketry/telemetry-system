import enum
from construct import Struct, BitStruct, Flag, BitsInteger, Padding, Enum, Byte, Int16ub, RawCopy, Switch, GreedyBytes, GreedyString, this
from .mqttsn_length_varint import MQTTSNLengthPrefixed


class MsgType(enum.IntEnum):
    ADVERTISE = 0x00
    SEARCHGW = 0x01
    GWINFO = 0x02
    CONNECT = 0x04
    CONNACK = 0x05
    WILLTOPICREQ = 0x06
    WILLTOPIC = 0x07
    WILLMSGREQ = 0x08
    WILLMSG = 0x09
    REGISTER = 0x0a
    REGACK = 0x0b
    PUBLISH = 0x0c
    PUBACK = 0x0d
    PUBCOMP = 0x0e
    PUBREC = 0x0f
    PUBREL = 0x10
    SUBSCRIBE = 0x12
    SUBACK = 0x13
    UNSUBSCRIBE = 0x14
    UNSUBACK = 0x15
    PINGREQ = 0x16
    PINGRESP = 0x17
    DISCONNECT = 0x18
    WILLTOPICUPD = 0x1a
    WILLTOPICRESP = 0x1b
    WILLMSGUPD = 0x1c
    WILLMSGRESP = 0x1d
    ENCASULATED = 0xfe

    def __str__(self) -> str:
        return f"{self._name_:<13}"


MQTTSNMessageAdvertise = Struct(
    "gateway_id" / Byte,
    "duration" / Int16ub,
)
MQTTSNMessageSearchGW = Struct(
    "radius" / Byte,
)
MQTTSNMessageGWInfo = Struct(
    "gateway_id" / Byte,
    "gateway_address" / GreedyBytes,
)
MQTTSNMessageConnect = Struct(
    "flags" / BitStruct(
        Padding(2),
        "clean_session" / Flag,
        "will" / Flag,
        Padding(4),
    ),
    "duration" / Int16ub,
    "client_id" / GreedyString("utf8"),
)

MQTTSNPacket = MQTTSNLengthPrefixed(
    Struct(
        "message_type" / Byte,
        "message" / (Switch(
            this.message_type,
            {
                MsgType.ADVERTISE: MQTTSNMessageAdvertise,
                MsgType.SEARCHGW: MQTTSNMessageSearchGW,
                MsgType.GWINFO: MQTTSNMessageGWInfo,
                MsgType.CONNACK: MQTTSNMessageConnect,
            },
            default=GreedyBytes,
        )),
    ))