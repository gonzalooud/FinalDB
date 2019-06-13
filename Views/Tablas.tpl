<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" >
    <tittle> </tittle>
</head>
<body>
<div class="container">
<table table-striped border="1">
    %for col_name in col_names:
         <td><b>{{col_name}}</b></td>
    %end

    %for row in rows:
        <tr>
        %for col in row:
            <td>{{col}}</td>
        %end
        </tr>
    %end
</table>
</div>
</body>
