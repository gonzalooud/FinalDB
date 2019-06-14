<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" >
    <tittle></tittle>
</head>
<body>
<ul class="nav bg-dark" aria-haspopup="true" aria-expanded="false">
  <li class="nav-item">
    <a class="nav-link active" href="/Principal">Home</a>
  </li>
  <li>
      <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Agregar nuevo Contribuyente
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <a class="dropdown-item" href="/NuevoJuridico">Juridico</a>
            <a class="dropdown-item" href="/NuevoFisico">Fisico</a>
        </div>
      </div>
  </li>
  <li>
    <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Modificar Contribuyente
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        <a class="dropdown-item" href="/ModificarJuridico">Juridico</a>
        <a class="dropdown-item" href="/ModificarFisico">Fisico</a>
        </div>
    </div>
  </li>
</ul>

<div class="container mt-5">
<form action="/consulta3" method="post">
  <div class="form-row">
    <div class="form-group col-md-6">
      <label for="inputDominio">Dominio</label>
      <input type="text" class="form-control" name="dominio" id="inputDominio" placeholder="Ingresar Dominio" required>
    </div>
  <button type="submit" class="btn btn-primary">Cargar</button>
</form>
</div>


<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
