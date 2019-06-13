<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" >
    <tittle></tittle>
</head>
<body>
<div class="container mt-5 pt-5" >
    <div class="mt-5 pt-5">
        <form action="/login" method="post">
          <div class="form-group">
            <label for="exampleInputUsuario">Usuario</label>
            <input type="text" class="form-control" id="exampleInputUsuario" name="username" placeholder="Ingresar Usuario">
          </div>
          <div class="form-group">
            <label for="exampleInputPassword1">Password</label>
            <input type="password" class="form-control" id="exampleInputPassword1" name="password" placeholder="Password">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</div>
</body>
