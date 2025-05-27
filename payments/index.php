<?php

// Roteamento simples para identificar o endpoint chamado
$request_uri = $_SERVER['REQUEST_URI'];

if ($request_uri === '/payment') {
    // Faz uma requisição HTTP para a API de Pedidos
    $orderJson = file_get_contents('http://orders:3002/order');
    $orderData = json_decode($orderJson, true);

    // Monta o JSON de resposta conforme o enunciado da prova
    $response = [
        'status' => 'paid',
        'order' => $orderData
    ];

    // Define o tipo de retorno como JSON
    header('Content-Type: application/json');
    // Retorna o JSON esperado
    echo json_encode($response);
} else {
    // Caso o endpoint não exista, retorna erro 404 em JSON
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
}
