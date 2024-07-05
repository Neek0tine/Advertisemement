 $(document).ready(function() {
   _V_("content").ready(function(){
      var myPlayer = this;
      myPlayer.on("progress", out_started);
  });
});

function out_started(){
  myPlayer =this;
  var myTextArea = document.getElementById('buffered');
  bufferedTimeRange=myPlayer.buffered();
  if ( (bufferedTimeRange.start(0)==0 ) && ( bufferedTimeRange.end(0) -  bufferedTimeRange.start(0) > 10 ) ){
       myPlayer.play();
  }

}