# Gerador de Descrição de Polígonos – QGIS

Plugin PyQGIS para extrair coordenadas dos vértices, calcular área e perímetro geodésicos e exportar relatório TXT.

## Funcionalidades

- Lista as camadas poligonais carregadas no projeto.
- Processa feições selecionadas ou todas as feições.
- Permite saída em SIRGAS 2000 geográfico (EPSG:4674) ou UTM 25S (EPSG:31985).
- Calcula área e perímetro com o elipsoide GRS80.
- Identifica anéis externos e internos e partes de MultiPolygon.
- Exporta arquivo TXT em UTF-8.
- Preserva a geometria original da camada.

## Instalação manual

1. Extraia a pasta `gerador_descricao_poligonos` para a pasta de plugins do perfil QGIS.
2. No QGIS, acesse **Complementos > Gerenciar e Instalar Complementos > Instalados**.
3. Ative **Gerador de Descrição de Polígonos**.
4. O ícone aparecerá na barra de ferramentas e no menu do plugin.

### Pasta de plugins no Windows

Normalmente:

`%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`

A pasta final deve ficar assim:

```text
plugins/
└── gerador_descricao_poligonos/
    ├── __init__.py
    ├── metadata.txt
    ├── plugin.py
    ├── icon.svg
    └── README.md
```

## Uso

1. Carregue uma camada poligonal no QGIS.
2. Se quiser, selecione as feições que deseja processar.
3. Clique no ícone do plugin.
4. Escolha a camada e o CRS de saída.
5. Marque “Processar somente feições selecionadas” se desejar.
6. Clique em **Gerar TXT** e escolha o local de gravação.

Se a opção de feições selecionadas estiver marcada, mas nenhuma feição estiver selecionada, o plugin processará todas as feições da camada.

## Sistemas de referência

- EPSG:4674 – SIRGAS 2000 geográfico (longitude/latitude).
- EPSG:31985 – SIRGAS 2000 / UTM zona 25S (Easting/Northing).

O EPSG:31985 é adequado à zona UTM cujo meridiano central é 33° W. O EPSG:4674 é geográfico e não utiliza meridiano central de projeção.

## Limitações

Esta versão não dissolve polígonos, não calcula azimutes ou distâncias de cada segmento, não identifica confrontantes e não gera memorial descritivo registral. A numeração dos vértices segue a ordem armazenada na geometria.

O relatório é auxiliar e deve ser conferido com a planta, o levantamento, as matrículas e as exigências da serventia. A quantidade de casas decimais não representa a acurácia do levantamento.

## Desenvolvimento

Versão: 1.0.0  
Requisito mínimo declarado: QGIS 3.16
