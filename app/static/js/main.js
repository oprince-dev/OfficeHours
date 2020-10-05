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
