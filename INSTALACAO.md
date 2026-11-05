# Instalação do plugin – Gerador de Descrição de Polígonos

Instruções para instalar, ativar, atualizar e remover o plugin **Gerador de Descrição de Polígonos** (versão 1.0.0) no QGIS.

> O plugin ainda não está publicado no repositório oficial de complementos do QGIS. Por enquanto, a instalação é feita a partir do arquivo ZIP ou da cópia manual da pasta.

## 1. Requisitos

| Item | Requisito |
|---|---|
| QGIS | 3.16 ou superior, série 3.x (declarado em `metadata.txt`). Versão LTR recomendada. |
| Sistema operacional | Windows, Linux ou macOS (qualquer um que rode o QGIS 3.x) |
| Dependências externas | Nenhuma. O plugin usa apenas bibliotecas que já vêm com o QGIS (PyQGIS e Qt). |
| Dados de entrada | Camada vetorial poligonal (Polygon ou MultiPolygon) com SRC definido |

> **QGIS 4.x (Qt6):** a versão 1.0.0 não declara compatibilidade com Qt6 no `metadata.txt` e não foi testada no QGIS 4. Por isso, use o QGIS 3.x.

## 2. Obter o pacote

Baixe o arquivo **`gerador_descricao_poligonos_qgis.zip`** na raiz deste repositório:

1. Abra o arquivo no GitHub.
2. Clique em **Download raw file** (ícone de download).

Se preferir, use **Code → Download ZIP** para baixar o repositório completo e localize a pasta `gerador_descricao_poligonos/`.

> Não extraia o arquivo ZIP do plugin para instalar pelo método A. O QGIS precisa dele compactado.

O ZIP precisa ter esta estrutura, com a pasta do plugin no primeiro nível:

```text
gerador_descricao_poligonos_qgis.zip
└── gerador_descricao_poligonos/
    ├── __init__.py
    ├── metadata.txt
    ├── plugin.py
    ├── icon.svg
    └── README.md
```

## 3. Método A – Instalar a partir do ZIP (recomendado)

1. Abra o QGIS.
2. Acesse **Complementos → Gerenciar e instalar complementos…**
3. No painel à esquerda, clique em **Instalar a partir do ZIP**.
4. Em **Arquivo ZIP**, selecione `gerador_descricao_poligonos_qgis.zip`.
5. Clique em **Instalar complemento**.
6. Se aparecer um aviso de segurança sobre complementos de fontes não confiáveis, confirme apenas se o arquivo foi baixado deste repositório.
7. Ao terminar, o QGIS informa que o complemento foi instalado.

## 4. Método B – Instalação manual (copiar a pasta)

1. Feche o QGIS.
2. Copie a pasta `gerador_descricao_poligonos/` inteira para a pasta de complementos do seu perfil:

| Sistema | Caminho padrão (perfil `default`) |
|---|---|
| Windows | `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\` |
| Linux | `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/` |

3. A estrutura final deve ser esta:

```text
plugins/
└── gerador_descricao_poligonos/
    ├── __init__.py
    ├── metadata.txt
    ├── plugin.py
    ├── icon.svg
    └── README.md
```

4. Abra o QGIS novamente.

Para descobrir o caminho exato do seu perfil, use **Configurações → Perfis de usuário → Abrir pasta do perfil ativo** e entre em `python/plugins`. Se a pasta `plugins` não existir, crie-a.

> Erro comum: copiar uma pasta a mais. Por exemplo, `plugins/gerador_descricao_poligonos_qgis/gerador_descricao_poligonos/`. Nesse caso o QGIS não encontra o plugin, porque o `metadata.txt` precisa estar um nível abaixo de `plugins/`.

## 5. Ativar o plugin

1. Acesse **Complementos → Gerenciar e instalar complementos… → Instalados**.
2. Marque a caixa **Gerador de Descrição de Polígonos**.
3. Com o plugin ativo, aparecem:
   - o menu **Complementos → Gerador de Polígonos → Gerador de Descrição de Polígonos**;
   - a barra de ferramentas **Gerador de Polígonos**, com o ícone do plugin.

Se a barra de ferramentas não aparecer, clique com o botão direito em uma área vazia das barras do QGIS e marque **Gerador de Polígonos**.

## 6. Teste rápido após a instalação

1. Carregue uma camada poligonal com SRC definido (por exemplo, SIRGAS 2000 / UTM 25S, EPSG:31985).
2. Se quiser, selecione algumas feições.
3. Clique no ícone do plugin.
4. Escolha a camada e o SRC de saída: **EPSG:4674** (geográfico) ou **EPSG:31985** (UTM 25S).
5. Se quiser processar apenas a seleção, marque **Processar somente feições selecionadas**. Se nenhuma feição estiver selecionada, o plugin processa todas.
6. Clique em **Gerar TXT** e escolha onde salvar.
7. Abra o arquivo gerado e confira:
   - a identificação da camada e do SRC;
   - as partes e os anéis (externo e internos);
   - as coordenadas dos vértices;
   - a área e o perímetro.

Para conferir a medição, compare a área do relatório com a calculadora de campos do QGIS, usando `$area` com o elipsoide GRS80 configurado no projeto (**Projeto → Propriedades → Geral → Medidas**). Diferenças pequenas podem vir do método de cálculo (elipsoidal ou planimétrico) e do SRC usado.

## 7. Atualizar para uma nova versão

**Método A:** repita a instalação a partir do ZIP com o arquivo novo. O QGIS substitui a versão instalada. Depois, reinicie o QGIS.

**Método B:** feche o QGIS, apague a pasta `gerador_descricao_poligonos/` antiga dentro de `python/plugins/`, copie a nova e abra o QGIS.

Para confirmar a versão instalada, veja **Complementos → Gerenciar e instalar complementos… → Instalados → Gerador de Descrição de Polígonos**.

## 8. Desinstalar

1. Acesse **Complementos → Gerenciar e instalar complementos… → Instalados**.
2. Selecione **Gerador de Descrição de Polígonos**.
3. Clique em **Desinstalar complemento**.

Você também pode fechar o QGIS e apagar a pasta `gerador_descricao_poligonos/` dentro de `python/plugins/`.

## 9. Solução de problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| O plugin não aparece em **Instalados** | Pasta em nível errado, ou `metadata.txt` ausente | Confira a estrutura da seção 4. O `metadata.txt` deve estar em `plugins/gerador_descricao_poligonos/metadata.txt`. |
| "O complemento está quebrado" / erro Python ao ativar | Arquivos incompletos ou versão do QGIS incompatível | Reinstale pelo ZIP. Confira se o QGIS é 3.16 ou superior (série 3.x). Copie o erro completo do painel **Mensagens de log → Python** e abra uma *issue*. |
| O plugin aparece como incompatível no QGIS 4.x | Ainda não há compatibilidade declarada com Qt6 | Use o QGIS 3.x (LTR). |
| A lista de camadas fica vazia | Não há camada poligonal válida no projeto | Carregue uma camada Polygon ou MultiPolygon. Camadas de pontos e de linhas não aparecem. |
| Erro de SRC inválido | Camada sem SRC definido | Defina o SRC correto da camada (**Propriedades → Fonte**). Não use **Definir SRC** para "corrigir" as coordenadas: isso só troca o rótulo, sem reprojetar. |
| Aviso de geometria inválida | Autointerseção, vértices duplicados ou anel mal formado | Verifique com **Vetor → Ferramentas de geometria → Verificar validade**. Corrija em uma cópia da camada antes de gerar a descrição. |
| Não consegue salvar o TXT | Pasta sem permissão de escrita ou arquivo aberto em outro programa | Escolha outra pasta ou feche o arquivo. |

## 10. Observações técnicas

- O plugin não altera a camada de origem. As transformações de coordenadas são feitas em cópias das geometrias (`QgsGeometry(geom)`), usando o contexto de transformação do projeto.
- O número de casas decimais no relatório indica resolução numérica. Não indica precisão nem acurácia posicional do levantamento.
- O EPSG:31985 (UTM 25S, MC 33° W) só é adequado para áreas dentro do fuso 25. Para áreas no fuso 24, o EPSG:31984 ainda não está disponível como saída nesta versão.
- O relatório é um documento auxiliar. Ele não substitui o memorial descritivo assinado por profissional habilitado (com ART/RRT) e não garante a aceitação pela serventia de registro de imóveis.

## 11. Suporte

Para relatar problemas ou sugerir melhorias, abra uma *issue* no repositório e informe:

- a versão do QGIS e o sistema operacional;
- a versão do plugin;
- a mensagem de erro completa (painel **Mensagens de log → Python**);
- se possível, um conjunto de dados de teste mínimo que reproduza o problema.

Projeto independente, sem vínculo com o ONR. Licença: GNU GPL-2.0-or-later.
