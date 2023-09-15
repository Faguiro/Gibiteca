



window.onload = function () {
    $('.sugestoes').hide();

}

$(window).keydown(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        return false;
    }
});

let keyword = window.location.pathname.split("/")[2];
$('#search-input').val(keyword);

function performSearch() {
    const keyword = $('#search-input').val();
    window.location.href = `/search/${keyword}`;
}

$('#search-button').click(performSearch);

$('#search-input').on("keyup", function (event) {
    $('.sugestoes').show();
    console.log(event.which);
    autoComplete(event.which)
    if (event.which === 13) {
        event.preventDefault();
        performSearch();
        return false; // Impede o envio do formulário
    }
});

/* $('#search-input').on("mouseout", function () {
    $('.sugestoes').hide()
}); */

$('#search-input').on("mouseover", function () {
    $('.sugestoes').show()
});

$('.sugestoes').on("mouseout", function () {
    $('.sugestoes').hide()
});

$('.sugestoes').on("mouseover", function () {
    $('.sugestoes').show()
});

$('#comics-container').click(function (event) {
    if (event.target.className == 'card-img-top') {
        let id = event.target.parentElement.children[1].children[1].id;
        console.log(id);
        window.location.href = `/comic/${id}`;
    }
    if (event.target.className == 'card-title') {
        let id = event.target.nextElementSibling.id;
        console.log(event.target.nextElementSibling);
        window.location.href = `/comic/${id}`;
    }
    if (event.target.className == 'card-info') {
        let id = event.target.id;
        console.log(id);
        window.location.href = `/comic/${id}`;
    }
});

function searchComics(key, page) {
    checkPage(page)

    $.get(`/search?keyword=${key}&page=${page}`, function (data) {
        const comicsContainer = $('#comics-container');
        comicsContainer.empty();
        $('#current-page').text(page);

        data.forEach(function (comic) {
            const comicCard = `
                <div class="col-md-3">
                    <div class="card">
                        <img src="${comic.capa}" class="card-img-top" alt="${comic.titulo}">
                        <div class="card-body">
                            <h5 class="card-title">${comic.titulo}</h5>
                            <p class="card-info" id=${comic.id} >${comic.editora} | ${comic.id}</p>
                        </div>
                    </div>
                </div>
            `;

            comicsContainer.append(comicCard);


        });

    });
}

function loadSearchInfo(key, page) {
    $.get(`/search_info?keyword=${key}`, function (info) {
        const totalPages = info.total_pages;
        const totalResults = info.total_results;
        // Faça algo com o total de páginas e resultados, por exemplo, atualize elementos HTML
        $('#total-pages').text(totalPages);
        $('#total-results').text(totalResults);
        checkPage(page);
        return info;
    });
}
function loadAllInfo(page) {
    $.get(`/search_all`, function (info) {
        const totalPages = info.total_pages;
        const totalResults = info.total_results;
        // Faça algo com o total de páginas e resultados, por exemplo, atualize elementos HTML
        $('#total-pages').text(totalPages);
        $('#total-results').text(totalResults);
        checkPage(page);
        return info;
    });
}

function search_control(key, page) {
    checkPage(page);

    $('.next-search').click(function () {
        page++;
        searchComics(key, page);
    });

    $('.prev-search').click(function () {
        if (page > 1) {
            page--;
            searchComics(key, page);
        }
    });
}
function checkPage(page) {

    let total_pg = $('#total-pages').text()
    total_pg = parseInt(total_pg);
    if (page === total_pg) {
        $('.next-search').hide();
    } else {
        $('.next-search').show();
    }

    if (page === 1) {
        $('.prev-search').hide();
    } else {
        $('.prev-search').show();
    }
}

function autoComplete(palavra, dicionario) {
    $('.sugestoes').show();
    return Object.keys(dicionario).filter((chave) => {
        const chaveMinusculo = chave.toLowerCase();
        const palavraMinusculo = palavra.toLowerCase();
        return chaveMinusculo.includes(palavraMinusculo);
    });
}

let palavrasChave = {};

// Faça a requisição para obter o dicionário a partir da rota
fetch('/api/palavraschave')
    .then(response => response.json())
    .then(data => {
        palavrasChave = data;
        console.log(palavrasChave);
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });

const campo = document.querySelector('.campo');
const sugestoes = document.querySelector('.sugestoes');

campo.addEventListener('input', ({ target }) => {
    const dadosDoCampo = target.value;
    if (dadosDoCampo.length) {
        const autoCompleteValores = autoComplete(dadosDoCampo, palavrasChave);
        sugestoes.innerHTML = `
    ${autoCompleteValores.map((chave) => {
            return (
                `<li class="autoCompleteItem">
                <a href="/search/${chave}">${chave}: ${palavrasChave[chave]}</a>
            </li>`
            );
        }).join('')}`;
    } else {
        sugestoes.innerHTML = ''; // Limpa as sugestões se o campo estiver vazio
    }
});



/* login em comics */

$(document).ready(function () {

    //verificar se existe user salvo em localStorage
    let user = localStorage.getItem('user');
    if (user) {
        user = JSON.parse(user);
        $('#user').text(user.username);
        console.log(user.username)
    } else {
        $('#user').text('Visitante');
        console.log('visitante')
    }

    $(".user_menu").hide();
    // Adicione um evento de clique ao botão de login no menu de navegação
    $('#login-button').click(function () {
        // Abra o modal de login
        $('#login-modal').modal('show');
    });

    $("#login").submit(function(){
        const formData = {
            username: $('#username').val(),
            email: $('#email').val(),
            password: $('#password').val()
        };
        save_session(formData)

    })

    // Manipule o envio do formulário de login via AJAX
    $('#login-form').submit(function (event) {
        event.preventDefault();

        // Obtenha os dados do formulário
        const formData = {
            username: $('#username').val(),
            email: $('#email').val(),
            password: $('#password').val()
        };

        // Envie os dados para a API de login
        $.ajax({
            type: 'POST',
            url: '/api/login',
            data: formData,
            success: function (response) {
                if (response.success) {
                    // Redirecione o usuário após o login bem-sucedido
                    save_session(formData)
                } else {
                    // Exiba uma mensagem de erro
                    $('#login-error').text('Credenciais inválidas');
                }
            },
            error: function () {
                // Trate erros de solicitação
                $('#login-error').text('Erro ao processar a solicitação de login');
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    try {
        const loginButton = document.getElementById('login-button');
        const loginModal = document.getElementById('login-modal');
        const closeModal = document.getElementById('close-modal');

        // Abrir o modal quando o botão de login for clicado
        loginButton.addEventListener('click', function () {
            loginModal.style.display = 'block';
        });

        // Fechar o modal quando o botão de fechar for clicado
        closeModal.addEventListener('click', function () {
            loginModal.style.display = 'none';
        });

        // Fechar o modal se o usuário clicar fora dele
        window.addEventListener('click', function (event) {
            if (event.target === loginModal) {
                loginModal.style.display = 'none';
            }
        });
    }
    catch {

    }
});


//Salvar sessão do usuário em cookie
function save_session(formData) {
    const username = formData.username
    const email = formData.email
    const user = {
        username: username,
        email: email
    }
    localStorage.setItem('user', JSON.stringify(user));
    location.reload();
};

function remove_session() {
    localStorage.removeItem('user', JSON.stringify(user));
    location.reload();
}



function loadComics(page) {
    $.get(`/comics?page=${page}`, function (data) {
        const comicsContainer = $('#comics-container');
        console.log(data);
        comicsContainer.empty();
        $('#current-page').text(page);

        data.forEach(function (comic) {
            const comicCard = `
                    <div class="col-md-3">
                        <div class="card">
                            <img src="${comic.capa}" class="card-img-top" alt="${comic.titulo}">
                            <div class="card-body">
                                <h5 class="card-title">${comic.titulo}</h5>
                                <p class="card-info" id=${comic.id} >${comic.editora} | ${comic.id}</p>
                            </div>
                        </div>
                    </div>

                `;

            comicsContainer.append(comicCard);
        });
    });

}



$('.fa-circle-user').click(function () {
    $(".user_menu").toggle();
})

$('.logout').click(function () {
    $.ajax({
        type: 'get',
        url: '/api/logout',

        success: function (response) {
            if (response.success) {
                // Redirecione o usuário após o login bem-sucedido
                remove_session(user)
            } else {
                // Exiba uma mensagem de erro
                $('#login-error').text('Credenciais inválidas');
            }
        },
        error: function () {
            // Trate erros de solicitação
            $('#login-error').text('Erro ao processar a solicitação de login');
        }
    });
})

$(".login").click(function () {
    window.location.href = `/login`;
})




