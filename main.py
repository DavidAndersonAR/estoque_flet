import flet as ft
import pymysql


class Marcas(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page 
        self.page = ft.ScrollMode.AUTO

    

    def build(self):
        return ft.Column(
                
                [
                    ft.Container(
                        expand=1,
                        content=ft.Text("Container 1"),
                        bgcolor=ft.colors.GREEN_100,
                    ),
                    ft.Container(
                        expand=2, content=ft.Text("Container 2"), bgcolor=ft.colors.RED_100
                    ),
                ],
            ),

    def db_execute(self, query, params=[]):
        with pymysql.connect(host="127.0.0.1", user="root", password="26143024", database="GestaoEstoque", port=3010) as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
          
           

            return cur.fetchall()



    def select_categorias(self, select):
        result = self.db_execute(query=select)
        
        marcas = []
        for coluna in result:
            
            id = coluna[0]
            nome = coluna[1]
            descricao = coluna[2]
            

            marcas.append(
                ft.DataRow(
                    [
                        ft.DataCell(ft.Text(id)),
                        ft.DataCell(ft.Text(nome)),
                        ft.DataCell(ft.Text(descricao)),
                        ft.DataCell(ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            icon_color="blue400",
                                            icon_size=20,
                                            tooltip="Editar",
                                            data = coluna,
                                            on_click=lambda _: print("Clicou aqui")
                                        )
                        ),
                    ]
                )
            )
        
        return marcas

class Gestao(ft.UserControl):

    
    def main(page: ft.Page):
        search = ft.TextField(
            border_color="black",
            height=40,
            text_size=13,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
            hint_text="search")
        nome = ft.TextField(
            border_color="black",
            height=40,
            text_size=13,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
            hint_text="Nome")
        descricao = ft.TextField(
            border_color="black",
            height=40,
            text_size=13,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
            hint_text="Descrição")
        
        
        def open_add_banco(e):
            print(page.route)
            if page.route == "/Categorias":
                tabela = "Categoria"
            elif page.route == "/Marcas":
                tabela = "Marcas"
            elif page.route == "/Fornecedores":
                tabela = "Fornecedores"

            def close_add_banco(e):
                add_banco.open = False
                page.update()

            def limpa_campos():
                nome.value = ""
                descricao.value = ""
                page.update()

            
            add_banco = ft.CupertinoAlertDialog(
                title=ft.Text("Cupertino Alert Dialog"),
                content=ft.Column(
                    [
                        nome,
                        descricao

                    ]
                ),
                actions=[
                    ft.CupertinoDialogAction(
                        "SALVAR",
                        is_destructive_action=True, on_click= lambda e: db_execute(query=f"insert into {tabela}(nome, descricao)" " values(%s, %s)",params=[nome.value, descricao.value])
                    ),
                    ft.CupertinoDialogAction(text="Cancel", on_click=close_add_banco),
                ],
                
            )
            page.dialog = add_banco
            add_banco.open = True
            
            limpa_campos()
            page.update()
        
        
        
        
        page.title = "Gestão Estoque"
        page.theme_mode = "light"
        page.scroll = ft.ScrollMode.AUTO
        
        def select_categorias(select):
            result = db_execute(query=select)
            marcas = []
            for coluna in result:   
                id = coluna[0]
                nome = coluna[1]
                descricao = coluna[2]
                marcas.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(id)),
                            ft.DataCell(ft.Text(nome)),
                            ft.DataCell(ft.Text(descricao)),
                            ft.DataCell(ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                icon_color="blue400",
                                                icon_size=20,
                                                tooltip="Editar",
                                                data = coluna,
                                                on_click=lambda _: print("Clicou aqui")
                                            )
                            ),
                        ]
                    )
                )
            return marcas

        def select_produtos(select):
            result = db_execute(query=select)
            produtos = []
            for coluna in result:   
                id = coluna[0]
                titulo = coluna[1]
                categoria = coluna[2]
                marca = coluna[3]
                preco_custo = coluna[4]
                preco_venda = coluna[5]
                numero = coluna[6]
                quantidade = coluna[7]

                produtos.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(id)),
                            ft.DataCell(ft.Text(titulo)),
                            ft.DataCell(ft.Text(categoria)),
                            ft.DataCell(ft.Text(marca)),
                            ft.DataCell(ft.Text(preco_custo)),
                            ft.DataCell(ft.Text(preco_venda)),
                            ft.DataCell(ft.Text(numero)),
                            ft.DataCell(ft.Text(quantidade)),
                            ft.DataCell(ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                icon_color="blue400",
                                                icon_size=20,
                                                tooltip="Editar",
                                                data = coluna,
                                                on_click=lambda _: print("Clicou aqui")
                                            )
                            ),
                        ]
                    )
                )
            return produtos


        def db_execute(query, params=[]):
            print(query)
            print(params)
            if page.route == "/Marcas" and params == ['', '']:
                print("Não é para add ao banco")
            else:
                print("Aqui ja é")
                

                with pymysql.connect(host="127.0.0.1", user="root", password="26143024", database="GestaoEstoque", port=3010) as con:
                    cur = con.cursor()
                    cur.execute(query, params)
                    con.commit()
                
                

                    return cur.fetchall()

        def app_form_input_field(name: str, expand: int, regex: str):

            return ft.Container(
                expand=expand,
                height=45,
                bgcolor="#ebebeb",
                border_radius=6,
                padding=8,
                content=ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text(
                            value=name,
                            size=9,
                            color='black',
                            weight="bold",
                        
                        ),
                        ft.TextField(
                            border_color="transparent",
                            height=20,
                            text_size=13,
                            content_padding=0,
                            cursor_color="black",
                            cursor_width=1,
                            cursor_height=18,
                            color="black",
                            input_filter=ft.InputFilter(allow=True, regex_string=regex, replacement_string=""),
                            
                        )
                    ]

                )

            )

        def app_form_dropdawn_field(name: str, expand: int, tabela: str):
            result = db_execute(query=f"SELECT * FROM {tabela}")
            dropdawn = []
            for linhas in result:
                id = linhas[0]
                name = linhas[1]
                dropdawn.append(
                    ft.dropdown.Option(key=id, text=name)
                )
            
            return ft.Container(
                expand=expand,
                height=45,
                bgcolor="#ebebeb",
                border_radius=6,
             
                content=ft.Column(
                    controls=[
                        ft.Dropdown(
                            label=name,
                            text_size=13,
                            options=
                                dropdawn
                                
                            ,
                            expand=True,
                        )
                    ]

                )

            )


        def route_change(route):
            page.views.clear()
            
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            leading=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Fornecedores",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Fornecedores"),
                                    ),
                                    ft.ElevatedButton(
                                        "Produtos",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Produtos"),
                                        
                                        

                                    ),
                                    
                                    ft.ElevatedButton(
                                        "Marcas",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Marcas"),
                                    ),
                                    ft.ElevatedButton(
                                        "Categorias",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Categorias"),
                                    ),
                                    ft.ElevatedButton(
                                        "Entradas",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Entradas"),
                                    ),
                                    ft.ElevatedButton(
                                        "Saidas",
                                        style=ft.ButtonStyle(
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.BLACK,
                                                ft.MaterialState.FOCUSED: ft.colors.BLUE,
                                                ft.MaterialState.DEFAULT: ft.colors.BLACK,
                                            },
                                            bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.WHITE},
                                            padding={ft.MaterialState.HOVERED: 20},
                                            overlay_color=ft.colors.TRANSPARENT,
                                            elevation={"pressed": 0, "": 1},
                                            animation_duration=500,
                                            side={
                                                ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                                ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                            },
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                            },
                                        ),
                                        on_click=lambda _: page.go("/Saidas"),
                                    ),
                                    
                                ]
                            ),
                            leading_width=500,
                            center_title=False,
                            
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            actions=[
                                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                                
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text="Item 1"),
                                        ft.PopupMenuItem(),  # divider
                                        ft.PopupMenuItem(
                                            text="Checked item", checked=False, 
                                        ),
                                    ]
                                ),
                                
                            ],
                            
                        ),

                        
        
                    ],
                    scroll = ft.ScrollMode.AUTO
                    
                )
            )
            if page.route == "/Marcas":
                page.views.append(
                    ft.View(
                        "/Marcas",
                        [   
                            ft.AppBar(
                                title=ft.Text("Marcas"), 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                actions=[
                                    ft.ElevatedButton("Nova Marca",icon=ft.icons.ADD, color='green', on_click=open_add_banco)]),
                            ft.Row(
                                width=500,
                                controls=[
                                    search,
                                    ft.ElevatedButton("Search", icon=ft.icons.SEARCH, on_click=lambda e: savedata(search))
                                ],
                        
                            ),
                            ft.Row(
                                [
                                    ft.DataTable(
                                        width=700,
                                        border=ft.border.all(2, "white"),
                                        border_radius=10,
                                        vertical_lines=ft.border.BorderSide(3, "blue"),
                                        horizontal_lines=ft.border.BorderSide(1, "green"),
                                        sort_column_index=0,
                                        sort_ascending=True,
                                        heading_row_color=ft.colors.BLACK12,
                                        heading_row_height=100,
                                        
                                    
                                        divider_thickness=0,
                                        columns=[
                                            ft.DataColumn(ft.Text("ID")),
                                            ft.DataColumn(ft.Text("NOME")),
                                            ft.DataColumn(ft.Text("DESCRIÇÃO")),
                                            ft.DataColumn(ft.Text("AÇÕES")),
                                        ],
                                        rows = select_categorias("SELECT * FROM Marcas")
                                    )
                                ]
                            )
                            
                        ],
                        scroll = ft.ScrollMode.AUTO
                    )
                    
                )
            elif page.route == "/Categorias":
                page.views.append(
                    ft.View(
                        "/Categorias",
                        [
                            
                            ft.AppBar(
                                title=ft.Text("Categorias"), 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                actions=[
                                    ft.ElevatedButton("Nova Categoria",icon=ft.icons.ADD, color='green', on_click=open_add_banco)
                                ]
                            ),
                            ft.Row(
                                width=500,
                                controls=[
                                    search,
                                    ft.ElevatedButton("Search", icon=ft.icons.SEARCH, on_click=lambda e: savedata(search))
                                ],
                        
                            ),
                            ft.Row(
                                [
                                    ft.DataTable(
                                        width=700,
                                        border=ft.border.all(2, "white"),
                                        border_radius=10,
                                        vertical_lines=ft.border.BorderSide(3, "blue"),
                                        horizontal_lines=ft.border.BorderSide(1, "green"),
                                        sort_column_index=0,
                                        sort_ascending=True,
                                        heading_row_color=ft.colors.BLACK12,
                                        heading_row_height=100,
                                        
                                    
                                        divider_thickness=0,
                                        columns=[
                                            ft.DataColumn(ft.Text("ID")),
                                            ft.DataColumn(ft.Text("NOME")),
                                            ft.DataColumn(ft.Text("DESCRIÇÃO")),
                                            ft.DataColumn(ft.Text("AÇÕES")),
                                        ],
                                        rows = select_categorias("SELECT * FROM Categoria")
                                    )
                                ]
                            )
                        ]
                    )
                )
            elif page.route == "/Fornecedores":
                page.views.append(
                    ft.View(
                        "/Fornecedores",
                        [
                            ft.AppBar(
                                title=ft.Text("Fornecedores"), 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                actions=[
                                    ft.ElevatedButton("Nov Fornecedor",icon=ft.icons.ADD, color='green', on_click=open_add_banco)
                                ]
                            ),
                            ft.Row(
                                width=500,
                                controls=[
                                    search,
                                    ft.ElevatedButton("Search", icon=ft.icons.SEARCH, on_click=lambda e: savedata(search))
                                ],
                        
                            ),
                            ft.Row(
                                [
                                    ft.DataTable(
                                        width=700,
                                        border=ft.border.all(2, "white"),
                                        border_radius=10,
                                        vertical_lines=ft.border.BorderSide(3, "blue"),
                                        horizontal_lines=ft.border.BorderSide(1, "green"),
                                        sort_column_index=0,
                                        sort_ascending=True,
                                        heading_row_color=ft.colors.BLACK12,
                                        heading_row_height=100,
                                        
                                    
                                        divider_thickness=0,
                                        columns=[
                                            ft.DataColumn(ft.Text("ID")),
                                            ft.DataColumn(ft.Text("NOME")),
                                            ft.DataColumn(ft.Text("DESCRIÇÃO")),
                                            ft.DataColumn(ft.Text("AÇÕES")),
                                        ],
                                        rows = select_categorias("SELECT * FROM Fornecedores")
                                    )
                                ]
                            )
                        ]
                    )
                )
            elif page.route == "/Produtos":
                page.views.append(
                    ft.View(
                        "/Produtos",
                        [
                            ft.AppBar(
                                title=ft.Text("Produtos"), 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                actions=[
                                    ft.ElevatedButton("Novo Produto",icon=ft.icons.ADD, color='green', on_click=lambda _: page.go("/add_produto"))
                                ]
                            ),
                            ft.Row(
                                width=500,
                                controls=[
                                    search,
                                    ft.ElevatedButton("Search", icon=ft.icons.SEARCH, on_click=lambda e: savedata(search))
                                ],
                        
                            ),
                            ft.Row(
                                [
                                    ft.DataTable(
                                        width=1000,
                                        border=ft.border.all(5, "orange"),
                                        border_radius=10,
                                        vertical_lines=ft.border.BorderSide(3, "blue"),
                                        horizontal_lines=ft.border.BorderSide(1, "green"),
                                        sort_column_index=0,
                                        sort_ascending=True,
                                        heading_row_color=ft.colors.BLACK12,
                                        heading_row_height=100,
                                        
                                    
                                        divider_thickness=0,
                                        columns=[
                                            ft.DataColumn(ft.Text("ID")),
                                            ft.DataColumn(ft.Text("Titulo")),
                                            ft.DataColumn(ft.Text("Categoria")),
                                            ft.DataColumn(ft.Text("Marca")),
                                            ft.DataColumn(ft.Text("Preço de custo")),
                                            ft.DataColumn(ft.Text("Preço de venda")),
                                            ft.DataColumn(ft.Text("Numero de serie")),
                                            ft.DataColumn(ft.Text("Quantidade")),
                                            ft.DataColumn(ft.Text("Ações")),
                                        ],
                                        rows = select_produtos("SELECT * FROM Produtos")
                                    )
                                ]
                            )
                        ]
                    )
                )
            
            elif page.route == "/add_produto":
                # limpa todos os campos dos textFields
                def clear_text_fields(controls):
                    for control in controls:
                        if isinstance(control, ft.Row):
                            for teste in control.controls:
                                if isinstance(teste, ft.Container):
                                    #teste.content.controls[1].value=""
                                    pass
                    page.update()
                # Recebe e trata os valores dos textfields
                def find_get_text(controls):
                    produto = []
                    for control in controls:
                        if isinstance(control, ft.Row):
                            for teste in control.controls:
                                if isinstance(teste, ft.Container):
                                    for text in teste.content.controls:
                                        
                                        if isinstance(text, ft.TextField):
                                            
                                            produto.append(text.value)
                                            
                                        elif isinstance(text, ft.Dropdown):
                                            produto.append(int(text.value))
                    print(produto)
                    db_execute(query="insert into Produtos(titulo, categoria, marca, preco_de_custo, preco_de_venda, numero_de_serie, quantidade) values(%s,%s,%s,%s,%s,%s,%s)", params=produto)
                                   
                                           

                page.views.append(
                    ft.View(
                        "/add_produto",
                        [
                            ft.AppBar(
                                title=ft.Text("Adicionar Produtos"), 
                                bgcolor=ft.colors.SURFACE_VARIANT, 
                                actions=[
                                    ft.ElevatedButton("Novo Produto",icon=ft.icons.ADD, color='green')
                                ]
                            ),
                            ft.Column(
                                controls=[
                                    
                                    ft.Row(
                                        controls=[
                                            app_form_input_field("Titulo *", 3, r"[0-9a-zA-Z]"),
                                            app_form_dropdawn_field("Categorias", 1, "Categoria"),
                                            app_form_dropdawn_field("Marcas", 1, "Marcas"),
                                            
                                        ],
                                    ), 
                                    ft.Row(
                                        controls=[
                                            app_form_input_field("Preço de custo *", 3, r"[0-9.,]"),
                                            app_form_input_field("Preço de venda *", 1, r"[0-9.,]"),
                                            app_form_input_field("Numero de serie *", 1, r"[0-9a-zA-Z]"),
                                            app_form_input_field("Quantidade *", 1, r"[0-9.,]"),
                                        ],
                                    ), 
                                    
                                ]
                            ),
                            ft.ElevatedButton("Adicionar", on_click=lambda e: (find_get_text(page.views[1].controls[1].controls), clear_text_fields(page.views[1].controls[1].controls))) # manda para a função certa e pega os dados dos textfields    
                        ]
                    )
                )
            page.update()


        def savedata(e):
             
            print(search.value)
            print(e.value)
            search.value = ""
            page.update()
            

        def view_pop(view):
                page.views.pop()
                top_view = page.views[-1]
                page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

        


        
    ft.app(target=main)