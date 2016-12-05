function viewComments(){
	 jQuery('#comments1').fadeIn("slow");
}
function postComment(){
	var commentContent=document.getElementById("comment-textbox").value;
	var testName=document.getElementById('userName').innerHTML;
	document.getElementById("comment-outer-container").innerHTML+='<div class="comment-container"><div class="Comment-User-ID" >'+testName+'</div><div class="Comment-content" >'+commentContent+'</div></div>';
   document.getElementById("comment-textbox").value="Type a comment...";
   	// document.getElementById("comments1").innerHTML+='    <div class="input-group"> <input type="text" class="form-control" placeholder="Type a comment..." id="comment-textbox" aria-describedby="input-comment"> <span class="input-group-addon" id="input-comment"><button onclick="postComment();" class="post-comment-button">POST</button></span> </div>';
                               
}