<?php

if ($_POST["pincode"] === "2374") {
	http_response_code(200);
}
 else{
 	http_response_code(401);
 }