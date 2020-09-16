import React from 'react'

export default function Header() {
    return (
        
    <nav class="navbar navbar-default header_area">
        <div class="container-fluid p0">
            <div  class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#header_collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span  class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.php"><p style="font-size:34px; color:white;  font-style: italic;   font-family: myFirstFont; ">ALITKAN</p></a>
            </div>

             <div class="collapse navbar-collapse" id="header_collapse">
                <ul class="nav navbar-nav navbar-right navbar_menu">
                    <li><a href="index.php">Home</a></li>
                    
        
                    <li class="dropdown submenu">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">services<i class="fa fa-angle-down"></i></a>
                        <ul class="dropdown-menu">
                            <li><a href="tops.php">tops</a></li>
                            <li><a href="acts.php">acts</a></li>
                            <li><a href="agencies.php">agencies</a></li>
                            
                        </ul>
                    </li>  
                     <li class="dropdown submenu">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Brands<i class="fa fa-angle-down"></i></a>
                        <ul class="dropdown-menu">
                                                        <li><a target="_blank" href="https://www.healthcare.siemens.com/">Siemens</a></li>
                                                        <li><a target="_blank" href="https://www.getinge.com/">GETINGE</a></li>
                                                        <li><a target="_blank" href="http://www.enraf-nonius.com/">Enraf Nonius</a></li>
                                                        <li><a target="_blank" href="https://www.varian.com/">Varian</a></li>
                                                        <li><a target="_blank" href="https://www.iba-radiopharmasolutions.com">Iba</a></li>
                                                        <li><a target="_blank" href="https://www.karlstorz.com">Karl Storz</a></li>
                                                        <li><a target="_blank" href="http://www.mindray.com/en/index.html">Mindray</a></li>

                                                        
                                                    </ul>
                    </li>
                   
                    <li><a href="projects.php">Projects</a></li>
                    <li><a href="index.php#news">news</a></li>
                    

                         <li><a href="about.php">About</a></li>
                            <li><a href="contact.php">Contact Us</a></li>
                    <li class="dropdown submenu">
                           <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-search"></i></a> 
                             <div class="dropdown-menu search_here">
                            <div class="input-group">
                                <input type="text" class="form-control" placeholder="Search heare...">
                                <span class="input-group-addon"><i class="fa fa-search"></i></span>
                            </div>
                        </div> 
                    </li> 
                </ul> 
            </div>
        </div>
        </div>
    </nav> 

        
    )
}
