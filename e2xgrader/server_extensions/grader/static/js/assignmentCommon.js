$.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
       console.log($.parseJSON(response));
      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });