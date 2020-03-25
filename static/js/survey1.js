$(document).ready(function() {
  "use strict";


  // ----------for survey page ------------------
  var form = $("#survey-form");
  form.validate({
      errorPlacement: function errorPlacement(error, element) {
           element.before(error);
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
      },
      onfocusout: function(element) {
          $(element).valid();
      },
      highlight : function(element, errorClass, validClass) {
          $(element.form).find('.actions').addClass('form-error');
          $(element).removeClass('valid');
          $(element).addClass('error');
      },
      unhighlight: function(element, errorClass, validClass) {
          $(element.form).find('.actions').removeClass('form-error');
          $(element).removeClass('error');
          $(element).addClass('valid');
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
          var myObj = {
              "gender":null,
              "age":null,
              "race":null,
              "nationality":null,
              "residential":null,
              "occupation":null,
              "martial":null,
              "vehicle":null,
              "income":null,
          };
          var temp = document.getElementsByName('gender');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.gender =temp[i].value;
              }
          }
          var temp = document.getElementsByName('age');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.age =temp[i].value;
              }
          }
          var temp = document.getElementsByName('race');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.race =temp[i].value;
              }
          }
          var temp = document.getElementsByName('residential_status');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.residential =temp[i].value;
              }
          }
          var temp = document.getElementsByName('occupation');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.occupation =temp[i].value;
              }
          }
          var temp = document.getElementsByName('marital_status');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.martial =temp[i].value;
              }
          }
          var temp = document.getElementsByName('vechicle_type');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.vehicle =temp[i].value;
              }
          }
          var temp = document.getElementsByName('time_type');
          for (var i = 0; i < temp.length; i++) {
              if(temp[i].checked){
                  myObj.income =temp[i].value;
              }
          }
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            myObj.nationality = document.getElementById('nat_input').value;
          $.ajax({
             type:"POST",
              headers:{
                "X-CSRFToken":csrftoken,
              },
             contentType:"application/json",
             url:'',
             data: JSON.stringify(myObj),
             dataType: "json",
             success:function (data) {
                 window.location.href = "/settings/account";
             },
             statusCode:{
                 404:function () {
                     window.location.href = "/settings/account";
                 }
             }
          });
      },
      // onInit : function (event, currentIndex) {
      //     event.append('demo');
      // }
  });


  $(document).ready(function(){
      $('.custom-control-input').click(function() {
          $('.custom-control-input').not(this).prop('checked', false);
          $(this).prop('checked',true);
      });
  });

  $('#nationality').click(function () {
    $('#nat_input').removeAttr('disabled');
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


});



