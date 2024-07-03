import os
from pyhanko import stamp
from pyhanko.pdf_utils import text
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers
from pyhanko.sign import timestamps
from pyhanko.sign.fields import SigSeedSubFilter
import uuid

pfx = '/home/micraow/sec/cert.pfx'  # 证书位置
passwd = b'填到这里'  # 密码
output_dir = '/home/micraow/Documents/signed/'  # 签名后的存放处，确保存在！
signer_name = 'Pengbo' # 签章人姓名
url = 'https://pengs.top' # 主页地址
email = 'peng@pengs.top' # 邮箱地址
extra_info = 'GPG fingerprint: \n6B5314F24B17198DD24B\n5B47062C2BFFBDCBB303\n' # 另外的想打印的信息
font_location = '/home/micraow/.local/Rajdhani-Medium.ttf' # 字体位置

signer = signers.SimpleSigner.load_pkcs12(
    pfx_file=pfx, passphrase=passwd
)

timestamper = timestamps.HTTPTimeStamper(
    url='https://freetsa.org/tsr'
)

in_file = input("Location of input pdf: ").strip()

target = input('Who is this document given to? (Myself by default) ').strip()

if target == '':
    target = 'Myself'

purpose = input(
    'The reason why you want to sign the document?(Not Specified by default) ').strip()

if purpose == '':
    purpose = 'Not Specified'

desc = input('Any other information you want to give? If not, hit Enter.').strip()

filename = os.path.basename(in_file)

with open(in_file, 'rb') as inf:
    w = IncrementalPdfFileWriter(inf, strict=False)
    fields.append_signature_field(
        w, sig_field_spec=fields.SigFieldSpec(
            # x1,y1,x2,y2 left to right, bottom to top
            'Signature', box=(395, 750, 580, 830)
        )
    )

    meta = signers.PdfSignatureMetadata(field_name='Signature', md_algorithm='sha256',
                                        subfilter=SigSeedSubFilter.PADES, embed_validation_info=False, use_pades_lta=True,)
    pdf_signer = signers.PdfSigner(
        meta, timestamper=timestamper, signer=signer, stamp_style=stamp.QRStampStyle(
            # Let's include the URL in the stamp text as well
            stamp_text='Signed by: %(signer)s\nEmail: %(email)s\nTime: %(ts)s\nURL: '+ url + \
            '\nUUID: \n%(uuid)s\n' + extra_info,
            text_box_style=text.TextBoxStyle(
                font=opentype.GlyphAccumulatorFactory(font_location)  # 字体位置
            ),
        ),
    )

    id = uuid.uuid1()

    info = "如果你看到这段文字，它意味着这个文件经过了数字签名。\nIf you see this text, it means the document has been digitally signed.\n" + \
        "签名人 The signer: " + signer_name + '\n'+'原始文件名 Original filename: ' + \
        filename+'\n'+'文档接收方 Target: ' + target + \
        '\n'+'文档签名原因 Reason: ' + purpose + '\n'

    if desc != '':
        info = info + '更多信息 More information: ' + desc+'\n'

    info = info + '这个文档使用了由Pengbo提供的工具进行签名，有关该签名的细节你可以在https://pengs.top/pdf-sign/ 看到。\n This document is signed using the tools provided by Pengbo, details of which can be found at https://pengs.top/pdf-sign/.'
    with open(output_dir+"signed_"+filename, 'wb') as outf:
        # with QR stamps, the 'url' text parameter is special-cased and mandatory, even if it
        # doesn't occur in the stamp text: this is because the value of the 'url' parameter is
        # also used to render the QR code.
        pdf_signer.sign_pdf(
            w, output=outf,
            appearance_text_params={
                'signer': signer_name, 'email': email, 'url': info, 'uuid': str(id)}
        )

print("File at: "+output_dir+"signed_"+filename)
