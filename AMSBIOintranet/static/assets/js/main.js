!(function ($) {
  "use strict";

  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#header').outerHeight() - 17;
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function (e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        e.preventDefault();

        var scrollto = target.offset().top - scrolltoOffset;

        if ($(this).attr("href") == '#header') {
          scrollto = 0;
        }

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function () {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function (e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function (e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });

    $(document).click(function (e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Toggle .header-scrolled class to #header when page is scrolled
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });

  if ($(window).scrollTop() > 100) {
    $('#header').addClass('header-scrolled');
  }

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });

  $('.back-to-top').click(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

  //js for loading Technical Records data on button.html
  $(document).ready(function () {

    $('button[id^="getrecord"]').one('click', function () {
      var rec_id = $(this).val();
      if (rec_id.search(/[.]/g) > 0) {
        var new_tag = rec_id.replace(/[\s.]/g, "-");
        console.log(new_tag);
        $(this).attr("data-target", "#collapse" + new_tag);
        $(this).attr("aria-controls", "collapse" + new_tag);
        var div_body = document.getElementById("collapse" + rec_id);
        div_body.id = "collapse" + new_tag;
      }
      var record_body;
      record_body = document.querySelector("#techRecordBody" + CSS.escape($(this).val()));
      $.ajax({
        url: 'techrecords',
        type: 'get',
        data: {
          record_id: $(this).val()
        },
        success: function (response) {
          if (response.flag) {
            loadOneCategory(response.data1, response.data2)
          }
          else {
            loadTwoCategories(response.data1, response.data2, response.cat_1, response.cat_2)
          }
        },
        error: function (e){
          alert('Categories do not exist');
          console.log(e);
        }
      });
      function loadOneCategory(json1, json2) { // function to load the technical properties when only 1 category exists.
        console.log(json1, json2);
        const tbody = document.createElement("tbody");
        tbody.className = "labels";
        tbody.innerHTML = `<tr>
                            <td>Property </td>
                            <td>Description </td>
                          </tr>`;
        record_body.append(tbody);
        const innerbody = document.createElement("tbody");
        for (const [key, value] of Object.entries(json1)) {
          const tr = document.createElement("tr");
          const td1 = document.createElement("td");
          td1.innerHTML = `<strong>${key}</strong>`;
          const td2 = document.createElement("td");
          td2.textContent = `${value}`;
          td1.style.cssText = 'width: 20%;';
          td2.style.cssText = 'width: 80%; word-wrap: break-word; white-space:normal;';
          tr.appendChild(td1);
          tr.appendChild(td2);
          innerbody.append(tr)
          record_body.append(innerbody);
        }
      }

      function loadTwoCategories(json1, json2, cat1, cat2) { // function to load the technical properties when 2 categories exists.
        console.log(json1, json2);
        var cat = [cat1, cat2];
        var jsonlist = [json1, json2];
        for (var i = 0; i < cat.length; i++) {
          const tbody = document.createElement("tbody");
          tbody.className = "labels";
          tbody.innerHTML = `<tr>
                                <td colspan='2'>
                                  <label for="${cat[i]}" style="cursor: pointer;">${cat[i]}</label>
                                  <input type="checkbox" name="${cat[i]}" id="${cat[i]}" data-toggle="toggle">
                                </td>
                              </tr>`;
          record_body.append(tbody);
          const innerbody = document.createElement("tbody");
          innerbody.className = "hide";
          for (const [key, value] of Object.entries(jsonlist[i])) {
            const tr = document.createElement("tr");
            const td1 = document.createElement("td");
            td1.innerHTML = `<strong>${key}</strong>`;
            const td2 = document.createElement("td");
            td2.textContent = `${value}`;
            td1.style.cssText = 'width: 20%;';
            td2.style.cssText = 'word-wrap: break-word; width: 80%; white-space:normal;';
            tr.appendChild(td1);
            tr.appendChild(td2);
            innerbody.append(tr);
            record_body.append(innerbody);
          }
        }
        $('[data-toggle="toggle"]').change(function () {
          $(this).parents().next('.hide').toggle();
        });
      }
    });
  });

  // js for form submission at 'edit single product' page for product records table
  $(document).on('submit', '#ProdForm', function (e) {
    e.preventDefault();
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var formData = JSON.stringify($(this).serializeArray());
    $.ajax({
      url: 'formsubmit',
      type: 'post',
      data: {
        csrfmiddlewaretoken: csrf,
        data: formData
      },
      success: function (response) {
        var div_body = document.querySelector('#prodform_container');
        $(this).remove();
        div_body.innerHTML = `<div class="card" style="width: 15em; text-align: center; height: 5em; margin-bottom: 5px;">
                                <div style="margin: auto;">
                                  <strong>${response.msg}</strong>
                                </div>
                              </div>`;
      }
    });
  });

  // js for form submission at 'edit single product' page for technical records table
  $(document).on('submit', '#TechForm', function (e) {
    e.preventDefault();
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var formData = JSON.stringify($(this).serializeArray());
    $.ajax({
      url: 'formsubmit',
      type: 'post',
      data: {
        csrfmiddlewaretoken: csrf,
        data: formData
      },
      success: function (response) {
        var div_body = document.querySelector('#techform_container');
        $(this).remove();
        div_body.innerHTML = `<div class="card" style="width: 15em; text-align: center; height: 5em; margin-bottom: 10px;">
                                <div style="margin: auto;">
                                  <strong>${response.msg}</strong>
                                </div>
                              </div>`;
      }
    });
  });

  // js for form submission at 'add new supplier' page
  $(document).on('submit', '#NewSupplier', function (e) {
    e.preventDefault();
    $.ajax({
      url: 'AddNewSupplier',
      type: 'post',
      data:{
        comp_name: $('#comp_name').val(),
        acc_code: $('#acc_code').val(),
        curr_code: $('#curr_code').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(json){
        document.getElementById('NewSupplier').reset();
        if (json.c_name == "" && json.c_code == ""){
          alert("Please enter the details!")
        }
        else {
          var card = document.querySelector("#SuccessCard");
          card.innerHTML = `<div class="card" style="margin-right: 20%; width: 20em;">
                              <div style="margin: 5%; margin-bottom: 2%;">    
                                <h4><strong>${json.c_name}</strong></h4>
                                <h6 class="text-muted">${json.c_code}</h6>
                                <h6 class="text-muted">${json.cur}</h6>
                                <br>
                                <p class="text-success" style="text-align:center;">${json.msg}</p>
                              </div>
                            </div>`;
        }
      }
    });
  });

})(jQuery);