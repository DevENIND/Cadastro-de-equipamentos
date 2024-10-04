
lista_equipamentos=[
    {"id":1, "Desc":"Hidromentro de 500L", "NumSerie": "DCTM","Prefixo": "H500", "Status": "Ativo", "OS": "50000981", "Certificado": "ABC1", "DataProx": "31/08/2025", "Cam_Img": "https://http2.mlstatic.com/D_NQ_NP_622641-MLB71540935465_092023-O.webp"},
    {"id":2, "Desc":"Manometro Spped Teste", "NumSerie": "MAN-003","Prefixo": "975-MAN-003", "Status": "Ativo", "OS": "5000990", "Certificado": "DEF2", "DataProx": "30/12/2024", "Cam_Img": "https://cdn.awsli.com.br/2500x2500/837/837306/produto/46634104/3051c4dbda.jpg"},
    {"id":3, "Desc":"Manometro Digital", "NumSerie": "68764","Prefixo": "MAD", "Status": "Ativo", "OS": "50000991", "Certificado": "GHI3", "DataProx": "31/01/2025", "Cam_Img": "https://www.salcas.com.br/image/cache/catalog/produtos/manometro-digital-medidor-de-pressao-digital-lc10-480x548.jpg"},
    {"id":4, "Desc":"Hidrometro de 1500L", "NumSerie": "DCTM","Prefixo": "H1500", "Status": "Ativo", "OS": "50000993", "Certificado": "JKL4", "DataProx": "02/11/2024", "Cam_Img": "https://ipemsp.wordpress.com/wp-content/uploads/2020/08/hidrometro-1.jpg"},
    {"id":5, "Desc":"Trena de 5mt", "NumSerie": "43156/30","Prefixo": "TER", "Status": "Ativo", "OS": "50000994", "Certificado": "JKL4", "DataProx": "20/06/2025", "Cam_Img": "https://casadosoldador.com.br/files/products_images/5833/0107613---trena-vonder-a%C3%A7o-5m-auto-trava---vonder.webp"},
    {"id":6, "Desc":"Paquimetro", "NumSerie": "PAQ-001","Prefixo": "PAQ", "Status": "Ativo", "OS": "50000995", "Certificado": "JKL4", "DataProx": "02/10/2024", "Cam_Img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxAyPeYUBP7_VeF6bV3ZlZYWbQviy-ELa1iA&s"}
    ]


if __name__ == '__main__':
   qtdTotal = len(lista_equipamentos)
   qtdLinhas = 0
   qtdLinhas = int(ceil(9 / 4))
   
   print(qtdTotal)
   print(qtdLinhas)