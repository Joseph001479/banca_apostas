<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$host = "localhost";
$user = "root";
$pass = "";
$dbname = "gestao_banca";

$conn = new mysqli($host, $user, $pass, $dbname);

if ($conn->connect_error) {
    die(json_encode(["sucesso" => false, "erro" => "Erro na conexão com o banco"]));
}

$data = json_decode(file_get_contents("php://input"), true);

if (isset($data["nomeTime"], $data["valor"], $data["odds"], $data["resultado"], $data["ganho"])) {
    $nomeTime = $conn->real_escape_string($data["nomeTime"]);
    $valor = $data["valor"];
    $odds = $data["odds"];
    $resultado = $conn->real_escape_string($data["resultado"]);
    $ganho = $data["ganho"];

    $query = "INSERT INTO apostas (nomeTime, valor, odds, resultado, ganho) VALUES ('$nomeTime', $valor, $odds, '$resultado', $ganho)";

    if ($conn->query($query)) {
        echo json_encode(["sucesso" => true, "mensagem" => "Aposta salva com sucesso"]);
    } else {
        echo json_encode(["sucesso" => false, "erro" => "Erro ao inserir aposta"]);
    }
} else {
    echo json_encode(["sucesso" => false, "erro" => "Dados incompletos"]);
}

$conn->close();
?>
