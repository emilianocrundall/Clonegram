$(document).ready(function(){

    $('.followers').on('click', function(){
        $('#modalfollowers').slideToggle();
    });

    $('.following').on('click', function(){
        $('#modalfollowing').slideToggle();
    });
    $('#actions').on('click', function(){
        $('#modal_actions').slideToggle();
    });
    function ajax_call(url, form){
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        return $.ajax({
            type: 'POST',
            data: form,
            dataType: 'json',
            url: url,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if (respuesta.error){
                    $('.errores').css({display: 'block'});
                    $('.errores').html(respuesta.msj);
                }
                else if(respuesta.success){
                    $(location).attr('href', '/usuario/home');
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    }
    function ajax_call_image(url, form){
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        return $.ajax({
            type: 'POST',
            data: form,
            dataType: 'json',
            url: url,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if (respuesta.error){
                    $('.errores').css({display: 'block'});
                    $('.errores').html(respuesta.msj);
                }
                else if(respuesta.success){
                    $(location).attr('href', '/usuario/home');
                }
            },
            error: function(e){
                console.log(e);
            },
            cache: false,
            contentType: false,
            processData: false
        });
    }
    $('#submit_register').on('click', function(e){
        e.preventDefault();
        form = $('#register_form').serialize();
        ajax_call('/usuario/registrarse/', form1);
    });
    
    $('#submit_login').on('click', function(e){
        e.preventDefault();
        form1 = $('#login_form').serialize();
        ajax_call('/usuario/login/', form1);
    });

    $('#submit_post').on('click', function(e){
        e.preventDefault();
        form1 = $('#post_form').get(0);
        formData = new FormData(form1);
        ajax_call_image('/postear/', formData);
    });

    $('#custom_input').on('change',function(){
        if($('#custom_input').val().length !=0){
            $('#span').html('Archivo seleccionado');
        }
    });

    $('.s_input').keyup(function(){
        var datos = $(this).serialize();
        $.ajax({
            type: 'GET',
            data: datos,
            url: '/usuario/resultados/',
            dataType: 'json',
            success: function(respuesta){
                if(respuesta.success){
                    $('.results').css({display: 'block'});
                    var html_code = '<ul class="ul_results">';
                    for(const item in respuesta.objetos){
                        html_code += '<li class="li_results"><a class="a_results" href="/usuario/' + respuesta.objetos[item].id + '/perfil/">' + respuesta.objetos[item].username + '</a></li>';
                    }
                    html_code += '</ul>';
                    $('.results').html(html_code);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    $('.s_input').on('input', function(){
        if($(this).val() === ''){
            $('.results').css({display: 'none'});
            $('.a_results').css({display: 'none'});
            $('.ul_results').css({display: 'none'});
            $('.li_results').css({display: 'none'});
        }
    });
    
    $('.s_input').on('blur', function(){
        setTimeout(function(){
            $('.results').css({display: 'none'});
            $('.a_results').css({display: 'none'});
            $('.ul_results').css({display: 'none'});
            $('.li_results').css({display: 'none'});
        }, 2000);
    });

    $(".listado a img").hover(function(){
            $(this).fadeTo(400, 0.5);
        },
        function(){
            $(this).fadeTo(400, 1);
        }
    );

    $('.btnfollow').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var id = $('.btnfollow').attr('value');

        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/usuario/' + id + '/follow/',
            data: id,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if(respuesta.unfollowed){
                    $('#unfollow').hide();
                    $('#follow').css({display: 'block'});
                }else if (respuesta.followed){
                    $('#follow').hide();
                    $('#unfollow').css({display: 'block'});
                }
            },error: function(e){
                console.log(e);
            }
        });
    });
    $('.like').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var id = $(this).attr('value');
        var button = $(this);
        var button2 = $(this).closest('#like').find('.liked');
        var button3 = $(this).closest('#like').find('.deleted');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/' + id + '/likear/',
            data: id,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if(respuesta.liked){
                    button.hide();
                    button2.css({display: 'block'});
                }else if (respuesta.deleted){
                    button.hide();
                    button3.css({display: 'block'});
                }
            },error: function(e){
                console.log(e);
            }
        });
    });
    $('.guardar').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var id = $(this).attr('value');
        var button = $(this);
        var button2 = $(this).closest('#save').find('.saved');
        var button3 = $(this).closest('#save').find('.removed');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/' + id + '/guardar/',
            data: id,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if(respuesta.saved){
                    button.hide();
                    button2.css({display: 'block'});
                }else if (respuesta.removed){
                    button.hide();
                    button3.css({display: 'block'});
                }
            },error: function(e){
                console.log(e);
            }
        });
    });

    $('.cmt').on('click', function(e){
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var datos = $(this).closest('#comentar_form').serialize();
        var id = $(this).attr('value');
        var add_comment = $(this).closest('#pub_comment').find('.new_comment');
        var input = $(this).closest('#comentar_form').find('.input_pub');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/' + id + '/comentar/',
            data: datos,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(respuesta){
                if(respuesta.success){
                    input.val('');
                    var html_code = "<div class='comentario2_'>";
                    html_code += "<p id='second_p'>" + respuesta.info[0]['fecha'] + "</p>";
                    html_code += "<a href='/usuario/home/'><strong>" + respuesta.info[0]['user'] + "</strong></a>";
                    html_code += "<p id='first_p'>" + respuesta.info[0]['texto'] + "</p>";
                    html_code += "</div>";
                    add_comment.append(html_code);
                }
            },
            error: function(e){
                console.log(e);
            }
        });
    });
    $('#comentar').attr('disabled',true);
    $('.input_pub').on('keyup',function(){
        if($(this).val().length !=0)
            $('#comentar').attr('disabled', false);            
        else
            $('#comentar').attr('disabled',true);
    });
    /*setTimeout(function(){
        codigo
    }, 2000);*/
    var modalDiv = $(".modal-div");
    $(".open_modal").on("click", function(){
         $.ajax({
          url: $(this).attr("data-url"),
          success: function(data) {
            modalDiv.html(data);
            $("#modal_likes").modal();
          },
          error: function(e){
              console.log(e);
          }
        });
    });
});