
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2014-03-19
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>FNAT Web Portal</title>
    <style type="text/css" media="screen">
  * {
    margin: 0px 0px 0px 0px;
    padding: 0px 0px 0px 0px;
  }

  body, html {
    padding: 3px 3px 3px 3px;

    background-color: #D8DBE2;

    font-family: Verdana, sans-serif;
    font-size: 11pt;
    text-align: center;
  }

  div.main_page {
    position: relative;
    display: table;

    width: 800px;

    margin-bottom: 3px;
    margin-left: auto;
    margin-right: auto;
    padding: 0px 0px 0px 0px;

    border-width: 2px;
    border-color: #212738;
    border-style: solid;

    background-color: #FFFFFF;

    text-align: center;
  }

  div.page_header {
    height: 99px;
    width: 100%;

    background-color: #F5F6F7;
  }

  div.page_header span {
    margin: 15px 0px 0px 50px;

    font-size: 180%;
    font-weight: bold;
  }

  div.page_header img {
    margin: 3px 0px 0px 40px;

    border: 0px 0px 0px;
  }

  div.table_of_contents {
    clear: left;

    min-width: 200px;

    margin: 3px 3px 3px 3px;

    background-color: #FFFFFF;

    text-align: left;
  }

  div.table_of_contents_item {
    clear: left;

    width: 100%;

    margin: 4px 0px 0px 0px;

    background-color: #FFFFFF;

    color: #000000;
    text-align: left;
  }

  div.table_of_contents_item a {
    margin: 6px 0px 0px 6px;
  }

  div.content_section {
    margin: 3px 3px 3px 3px;

    background-color: #FFFFFF;

    text-align: left;
  }

  div.content_section_text {
    padding: 4px 8px 4px 8px;

    color: #000000;
    font-size: 100%;
  }

  div.content_section_text pre {
    margin: 8px 0px 8px 0px;
    padding: 8px 8px 8px 8px;

    border-width: 1px;
    border-style: dotted;
    border-color: #000000;

    background-color: #F5F6F7;

    font-style: italic;
  }

  div.content_section_text p {
    margin-bottom: 6px;
  }

  div.content_section_text ul, div.content_section_text li {
    padding: 4px 8px 4px 16px;
  }

  div.section_header {
    padding: 3px 6px 3px 6px;

    background-color: #8E9CB2;

    color: #FFFFFF;
    font-weight: bold;
    font-size: 112%;
    text-align: center;
  }

  div.section_header_red {
    background-color: #CD214F;
  }

  div.section_header_grey {
    background-color: #9F9386;
  }

  .floating_element {
    position: relative;
    float: left;
  }

  div.table_of_contents_item a,
  div.content_section_text a {
    text-decoration: none;
    font-weight: bold;
  }

  div.table_of_contents_item a:link,
  div.table_of_contents_item a:visited,
  div.table_of_contents_item a:active {
    color: #000000;
  }

  div.table_of_contents_item a:hover {
    background-color: #000000;

    color: #FFFFFF;
  }

  div.content_section_text a:link,
  div.content_section_text a:visited,
   div.content_section_text a:active {
    background-color: #DCDFE6;

    color: #000000;
  }

  div.content_section_text a:hover {
    background-color: #000000;

    color: #DCDFE6;
  }

  div.validator {
  }
    </style>
  </head>
  <body>
    <div class="main_page">
      <div class="page_header floating_element">
        <img src="/icons/flukenetworks-logo.png" alt="Fluke Networks Logo" class="floating_element"/>
        <span class="floating_element">
          FNAT Web Portal  
        </span>
      </div>

      <div class="content_section floating_element">


        <div class="section_header section_header_red">
          <div id="about"></div>
           Test Result
        </div>
        <?php
          $exec_id = $_GET['exec_id'];
          $mysql_conn = mysql_connect("localhost", "root", "123456");
          if(!$mysql_conn){
              echo "<div class=\"content_section_text\">";
              echo "<p>Fail to connect with Database</p>";
              echo "</div>";
          }
          mysql_select_db("fnat_base", $mysql_conn);
          $q = "SELECT * FROM fnat_execution WHERE exec_id=$exec_id";
          $rs = mysql_query($q, $mysql_conn);
          $row = mysql_fetch_row($rs);
          mysql_free_result($rs);

          echo "<div class=\"table_of_contents\"></div>";
          echo "<div class=\"section_header\"><div id=\"serial\"></div>Device: $row[3] ($row[1]) $row[2]</div>";
          echo "<div class=\"table_of_contents\"></div>";
          echo "<div class=\"content_section_text\">";
          echo "<table border=\"1px\" cellspacing=\"0px\" style=\"width:800px\">";

          $sql_query_execution = "SELECT * FROM fnat_case_result WHERE exec_id = $exec_id ORDER BY record_id";
          $rs_query_execution = mysql_query($sql_query_execution, $mysql_conn);
          while($row = mysql_fetch_row($rs_query_execution)){
              echo "<tr>";
              echo "<td style=\"width:500px\">$row[2]</td>";
              if(0 == $row[3]){
                  echo "<td style=\"width:250px\"><b><font color=\'#0F0\">PASS</font></b></td>";
              }
              else{
                  echo "<td style=\"width:250px\"><b><font color=\"#F00\">FAIL</font></b></td>";
              }
              echo "<td>Screenshot</td>";
              echo "</tr>";
          }
          mysql_free_result($rs_query_execution);
          echo "</table>";
          echo "</div>";

          mysql_close($mysql_conn);
        ?>

        <div class="section_header section_header_red">
          <div id="support"></div>
                Support Information
        </div>
        <div class="content_section_text">
          <p>
                <b>FNAT</b> (Fluke Networks Automation Test) system is used to track and manage 
                the automation test in Shanghai.
          </p>
          <p>
                You can always get support from:
          </p>
          <ul>
                <li>
                    WAN Lizhou (lizhouwan@hotmail.com)
                </li>
          </ul>
        </div>
      </div>
    </div>
  </body>
</html>

