$(document).ready(function() {
  "use strict";
  var form = $("#review-form");
  form.validate({
      errorPlacement: function errorPlacement(error, element) {
           // element.before(error); 
         var input = $('.incident-regarding .input200');
         console.log(input.length);
         for(var i=0; i<input.length; i++) {
           if(validate(input[i]) == false){
             // console.log('validate false');
             showValidate(input[i]);
           } else if(validate(input[i]) == true){
             console.log('validate true');
             hideValidate(input[i]);
           }
         }

         input = $('.review-regarding .input200');
         console.log(input.length);
         for(var i=0; i<input.length; i++) {
           if(validate(input[i]) == false){
             // console.log('validate false');
             showValidate(input[i]);
           } else if(validate(input[i]) == true){
             console.log('validate true');
             hideValidate(input[i]);
           }
         }
      },
      rules: {
          feeling : {
              required: true,
          },
          feedback_regarding : {
              required: true,
          },
          feedback_categories : {
              required: true,
          },
          bus_no : {
              required: true,
          },
          incident_date : {
              required: true,
          },
          incident_time : {
              required: true,
          },
          route_no : {
              required: true,
          },
          route_name : {
              required: true,
          },
          bus_operator : {
              required: true,
          },
          quick_review : {
              required: true,
          },
          event: {
              required: true,
          },
          comment: {
              required: true,
          },
      },
      onfocusout: function(element) {
          $(element).valid();
      },
      highlight : function(element, errorClass, validClass) {
          // $(element.form).find('.actions').addClass('form-error');
          // $(element).removeClass('valid');
          // $(element).addClass('error');
      },
      unhighlight: function(element, errorClass, validClass) {
          // $(element.form).find('.actions').removeClass('form-error');
          // $(element).removeClass('error');
          // $(element).addClass('valid');
      }
  });
  form.steps({
      headerTag: "h4",
      bodyTag: "section",
      transitionEffect: "fade",
      enablePagination: true,
      labels: {
          previous : '«',
          next : 'Next',
          finish : 'Submit',
          current : ''
      },
      titleTemplate : '<span class="title">#title#</span>',
      onStepChanging: function (event, currentIndex, newIndex)
      {
          form.validate().settings.ignore = ":disabled,:hidden";
          return form.valid();
      },
      onFinishing: function (event, currentIndex)
      {
          form.validate().settings.ignore = ":disabled";
          return form.valid();
      },
      onFinished: function (event, currentIndex)
      {
          $('#reviewSubmitModalForm').modal('show');
      },
      // onInit : function (event, currentIndex) {
      //     event.append('demo');
      // }
  });

  $('.input200').each(function(){
      $(this).on('blur', function(){
          if($(this).val().trim() != "") {
              $(this).addClass('has-val');
          }
          else {
              $(this).removeClass('has-val');
          }
      })    
  })

  function validate (input) {
    if($(input).val().trim() == ''){
        console.log('empty');
        return false;
    } else {
      console.log('not empty');
        return true;
    }
  }

  function showValidate(input) {
    var thisAlert = $(input).parent();

    $(thisAlert).addClass('alert-validate-2');
  }

  function hideValidate(input) {
      var thisAlert = $(input).parent();

      $(thisAlert).removeClass('alert-validate-2');
  }

  $('.incident-regarding .input200').each(function(){
    $(this).focus(function(){
       hideValidate(this);
    });
  });

  $('.review-regarding .input200').each(function(){
    $(this).focus(function(){
       hideValidate(this);
    });
  });

  jQuery.extend(jQuery.validator.messages, {
      required: "",
      remote: "",
      email: "",
      url: "",
      date: "",
      dateISO: "",
      number: "",
      digits: "",
      creditcard: "",
      equalTo: "",
      bus_no: "",
      incident_date: "",
      incident_time: "",
      route_no: "",
      route_name: "",
      bus_operator: "",
      quick_review: "",
      event: "",
      comment: "",
  });

  $(document).ready(function(){
      $('.custom-control-input').click(function() {
          $('.custom-control-input').not(this).prop('checked', false);
          $(this).prop('checked',true);
      });
  });

  
const labels = document.querySelectorAll('.label');
  for(var i = 1; i < labels.length-1; i++)
  {
      const chars = labels[i].textContent.split('');
       labels[i].innerHTML = '';
       chars.forEach(char => {
           labels[i].innerHTML += `<span>${char === ' ' ? '&nbsp' : char}</span>`;
       });
  }


  function initMap() {
    var mapProp= {
      center:new google.maps.LatLng(51.508742,-0.120850),
      zoom:5,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
  }

  $('#quick_review').parent().append('<ul  class="list-item" id="newpayment_type" name="quick_review"></ul>');
  $('#quick_review option').each(function(){
      $('#newpayment_type').append('<li value="' + $(this).val() + '' + '" data-symbol="' + '&#xf2f9;' + '">' + $(this).text()+'</li>');
  });
  $('#quick_review').remove();
  $('#newpayment_type').attr('id', 'quick_review');
  $('#quick_review li').first().addClass('init');
  $("#quick_review").on("click", ".init", function() {
      $(this).closest("#quick_review").children('li:not(.init)').toggle();
  });
  
  var PaymentsOptions = $("#quick_review").children('li:not(.init)');
  $("#quick_review").on("click", "li:not(.init)", function() {
      PaymentsOptions.removeClass('selected');
      $(this).addClass('selected');
      $("#quick_review").children('.init').html($(this).html());
      PaymentsOptions.toggle();
  });

  var imgUpload = document.getElementById('upload_imgs')
    , imgPreview = document.getElementById('img_preview')
    , imgUploadForm = document.getElementById('img-upload-form')
    , totalFiles
    , img;

  imgUpload.addEventListener('change', previewImgs, false);
  // imgUploadForm.addEventListener('submit', function (e) {
  //   e.preventDefault();
  //   alert('Images Uploaded! (not really, but it would if this was on your website)');
  // }, false);

  function previewImgs(event) {
    
    totalFiles = imgUpload.files.length;
    
    if(!!totalFiles) {
      // imgPreview.classList.remove('quote-imgs-thumbs--hidden');
      $(".active-post-carusel").remove();
      $('.carousel-wrapper').append('<div class="owl-carousel active-post-carusel quote-imgs-thumbs quote-imgs-thumbs--hidden" id="img_preview" aria-live="polite"></div>');
      var imgPreview = document.getElementById('img_preview');
    }
    

    for(var i = 0; i < totalFiles; i++) {
      img = document.createElement('img');
      img.src = URL.createObjectURL(event.target.files[i]);
      img.classList.add('img-preview-thumb');
      imgPreview.appendChild(img);
      console.log('imgs are added!');
    }

    $(".active-post-carusel").owlCarousel({
        items: 3,
        loop: true,
        margin: 0,
        dots: false,
        nav: true,
        // autoplay: 2500,
        navText: [
          // "<span class='lnr lnr-arrow-up'></span>",
          // "<span class='lnr lnr-arrow-down'></span>"
        ]
    });
  }
});



