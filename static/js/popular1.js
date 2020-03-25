$(document).ready(function() {
  "use strict";
  
  /*-----------------custom select box------------------*/
  $(".sortby-select-box").each(function() {
    var classes = $(this).attr("class"),
        id      = $(this).attr("id"),
        name    = $(this).attr("name");

    // template += '<a href="#" class="custom-option ' + $(this).attr("class") + '" data-value="' + $(this).attr("value") + '"><img src="img/happy.png" style="max-height: 15px;"/>' + $(this).html() +'<img src="img/angry.png"  style="max-height: 15px;"></a>'    

    var things = $(this).find("option");
    var template =  '<div class="' + classes + '">';
        template += '<span class="sortby-select-trigger">' + $(this).attr("placeholder") + '</span>';
        template += '<div class="custom-options">';
        template += '<a href="#" class="custom-option happy-feeling-wrapper d-flex flex-row" data-value="' + things[0].getAttribute("value") +'" value="1"><img src="/static/img/happy.png"/>' + '<span class="' + things[0].getAttribute("class") + '">&nbsp;TO&nbsp;</span>' + '<img src="/static/img/angry.png"></a>';
        template += '<a href="#" class="custom-option happy-feeling-wrapper d-flex flex-row" data-value="' + things[1].getAttribute("value") +'" value="2"><img src="/static/img/angry.png"/>' + '<span class="' + things[1].getAttribute("class") + '">&nbsp;TO&nbsp;</span>' + '<img src="/static/img/happy.png"></a>';
        template += '<a href="#" class="custom-option" data-value="'+ things[2].getAttribute("value") + '"value="3"><span class="' + things[2].getAttribute("class") + '">' + things[2].innerHTML + '</span></a>';
        template += '<a href="#" class="custom-option" data-value="'+ things[3].getAttribute("value") + '"value="4"><span class="' + things[3].getAttribute("class") + '">' + things[3].innerHTML + '</span></a>';
        template += '</div></div>';
    
    $(this).wrap('<div class="custom-select-wrapper"></div>');
    $(this).hide();
    $(this).after(template);
  });


  $(".sortby-select-box .custom-option:first-of-type").hover(function() {
    $(this).parents(".custom-options").addClass("option-hover");
  }, function() {
    $(this).parents(".custom-options").removeClass("option-hover");
  });
  $(".sortby-select-trigger").on("click", function() {
    $('html').one('click',function() {
      $(".sortby-select-box").removeClass("opened");
    });
    $(this).parents(".sortby-select-box").toggleClass("opened");
    event.stopPropagation();
  });
  $(".sortby-select-box .custom-option").on("click", function() {
    console.log($(this).attr("data-value"));
    $(this).parents(".custom-select-wrapper").find("select").val($(this).data("value"));
    $(this).parents(".custom-options").find(".custom-option").removeClass("selection");
    $(this).addClass("selection");
    $(this).parents(".sortby-select-box").removeClass("opened");
    $(this).parents(".sortby-select-box").find(".sortby-select-trigger").text($(this).attr("data-value"));
  });


  $(".viewby-select-box").each(function() {
    var classes = $(this).attr("class"),
        id      = $(this).attr("id"),
        name    = $(this).attr("name");
    var template =  '<div class="' + classes + '">';
        template += '<span class="viewby-select-trigger">' + $(this).attr("placeholder") + '</span>';
        template += '<div class="custom-options">';
        $(this).find("option").each(function() {
          template += '<span class="custom-option ' + $(this).attr("class") + '" data-value="' + $(this).attr("value") + '">' + $(this).html() + '</span>';
        });
    template += '</div></div>';
    
    $(this).wrap('<div class="custom-select-wrapper"></div>');
    $(this).hide();
    $(this).after(template);
  });

  $(".viewby-select-box .custom-option:first-of-type").hover(function() {
    $(this).parents(".custom-options").addClass("option-hover");
  }, function() {
    $(this).parents(".custom-options").removeClass("option-hover");
  });

  $(".viewby-select-box .custom-option").on("click", function() {
    console.log($(this).attr("data-value"));
    $(this).parents(".custom-select-wrapper").find("select").val($(this).data("value"));
    $(this).parents(".custom-options").find(".custom-option").removeClass("selection");
    $(this).addClass("selection");
    $(this).parents(".viewby-select-box").removeClass("opened");
    $(this).parents(".viewby-select-box").find(".viewby-select-trigger").text($(this).text());
  });

  $(".viewby-select-trigger").on("click", function() {
    $('html').one('click',function() {
      $(".viewby-select-box").removeClass("opened");
    });
    $(this).parents(".viewby-select-box").toggleClass("opened");
    event.stopPropagation();
  });
  $(".custom-option.undefined").on('click', function () {
      var selected = $(".custom-option.undefined.selection").attr('data-value');
      if(selected == 1){
          window.location.href = '/mapview';
      }
  });

});



