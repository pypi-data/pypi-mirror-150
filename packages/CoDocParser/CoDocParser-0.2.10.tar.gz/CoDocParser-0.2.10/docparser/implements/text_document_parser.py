import os

from parse import parse

from docparser.core.document_parser_base import DocumentParserBase


class TextDocumentParser(DocumentParserBase):
    """
    文本文件解析器
    """

    def __init__(self, file, configs):
        """
        初始化
        :param file:文件路径
        :param configs: 配置
        """
        self._file = file
        self._configs = configs

        if not os.path.exists(file):
            raise FileNotFoundError
        with open(file, 'r') as f:
            self._data = f.readlines()

    def parse(self):
        """
        根据配置抽取数据
        :return: 返回抽取的数据
        """

        data_bucket = {}
        results= []
        for key in self._configs.keys():
            item_config = self._configs[key]
            for m in self._data:
                for m_parse in item_config['parse']:
                    result = parse(m_parse.rstrip(), m)
                    if result is not None:
                        results.append(result)
                        for kv,val in result.named.items():
                            data_bucket[kv] = str(val).strip()
                    # print(m, m_parse, result)

        return data_bucket


if __name__ == '__main__':
    converter = TextDocumentParser(
        r"C:\Users\RobinJiang\Desktop\shz4984677-de9f1f851296083ce0530a0087608d96.txt",
        {
            'standard': {
                'parse':
                    [r'Shipping Order No.:{so}Booking Date:Electronic Ref.: {bookDate} {electronicRef}',
                     r'Shipper / Forwarder:  {shipper}',
                     r'PIC: {pic}',
                     r'Deciding Party:  {deciding_party} SCAC Code :  {scac_code}',
                     r'B/L Number :  {billno}',
                     r'Vessel/Voyage:  {vessel_voyage}',
                     r'Place of Receipt: {place_of_receipt} Alternate Base Pool:{alternate_base_pool} Ramp Cut-Off Date/Time:{ramp_cutoff_datetime}',
                     r'Feeder Vessel/Voyage:{feeder_vessel_voyage} ETD: {first_etd}',
                     r'Port of Loading: {port_of_loading}  ETD: {second_etd}',
                     r'Loading Terminal:  {loading_terminal}  Cargo Receiving Date: {cargo_receiving_date}',
                     r'VGM Cut-Off Date/Time: {vgm_cutoff_datetime}',
                     r'Discharge Instruction:{discharge_instruction} Transhipment Port:{transhipment_port}  Port Cut-off Date/Time:{port_cutoff_datetime} SI Cut-off Date/Time: {si_cutoff_datetime} ',
                     r'Port of Discharge:  {port_of_discharge}  Booking Pty. Ref.: {booking_pty_ref}',
                     r'Place of Delivery: {place_of_delivery}',
                     r'ENS Clause: {ens_clause} ETA: {eta} SI Fax No.: {si_fax_no} SI Email: {si_email} Vessel Flag: {vessel} IMO: {imo} Country of Documentation: {doc} Operator: {operator}',
                     r'{container_type}GP WITHOUT VENTILATION HC X{container_num:d} {weight:f}']
            }
        })
    data = converter.parse()
    print(data)
