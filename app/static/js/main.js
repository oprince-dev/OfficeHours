/// Leftnav ///
$(function() {
  $('#classes-item').click(function() {
    $('#leftnav-icons-pane').children().removeClass('active');
    $(this).addClass('active');
    $('#leftnav-submenu-pane').children().hide();
    $('#classes-pane').show();
  });
  $('#week-item').click(function() {
    $('#leftnav-icons-pane').children().removeClass('active');
    $(this).addClass('active');
    $('#leftnav-submenu-pane').children().hide();
    $('#week-pane').show();
  });
  $('#whiteboard-item').click(function() {
    $('#leftnav-icons-pane').children().removeClass('active');
    $(this).addClass('active');
    $('#leftnav-submenu-pane').children().hide();
    $('#whiteboard-pane').show();
  });
  $('#onlineroom-item').click(function() {
    $('#leftnav-icons-pane').children().removeClass('active');
    $(this).addClass('active');
    $('#leftnav-submenu-pane').children().hide();
    $('#onlineroom-pane').show();
  });
  $('#helpdesk-item').click(function() {
    $('#leftnav-icons-pane').children().removeClass('active');
    $(this).addClass('active');
    $('#leftnav-submenu-pane').children().hide();
    $('#helpdesk-pane').show();
  });
});
/// Add Student ///
// Keyup search results
$(function() {
  $("#studentFilterInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#studentFilterBody tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
// Click to add to form
$(function() {
  $("#studentFilterBody > tr").on("click", function() {
    var id = $(this).find("td:eq(0)").text()
    var first = $(this).find("td:eq(1)").text()
    var last = $(this).find("td:eq(2)").text()
    $("#addStudentForm > div.form-group > input#student_id").val(id)
    $("#addStudentForm > div.form-group > input#first").val(first)
    $("#addStudentForm > div.form-group > input#last").val(last)
  });
});
$(function() {
  $("#upload_students_submit").on("click", function() {
    var form_data = new FormData($('#upload_students')[0]);
    $.ajax({
      type: 'POST',
      url: '/add/student/upload',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function(data) {
        $('#fileStudentsTable > thead').children().remove();
        $('#fileStudentsTable > tbody').children().remove();
        $('#fileSudentsTableContainer').show();
        trh = $('<tr/>');
        console.log(data.table_columns)
        $.each(data.table_columns, function(i, head) {
          console.log(head);
          trh.append('<th>' + head + '</th>');
          $("#fileStudentsTable > thead").append(trh);
        })
        $.each(data.file_students, function(i, obj) {
          tr = $('<tr/>');
          console.log(obj)
          tr.append('<td><input type="hidden" name="first" value="'+ obj.First +'" >' + obj.First + '</input></td>');
          tr.append('<td><input type="hidden" name="last" value="'+ obj.Last +'" >' + obj.Last + '</input></td>');
          tr.append('<td><input type="hidden" name="email" value="'+ obj.Email +'" >' + obj.Email + '</input></td>');
          tr.append('<td><input type="hidden" name="DOB" value="'+ obj.DOB +'" >' + obj.DOB + '</input></td>');
          $("#fileStudentsTable > tbody").append(tr);
        });
      },
    });
  });
});
