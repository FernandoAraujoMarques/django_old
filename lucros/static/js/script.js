    // Obter o elemento h1
    var lucroElement = document.getElementById("lucro");

    // Obter o texto do elemento h1
    var lucroText = lucroElement.textContent;

    // Remover os zeros desnecessários usando parseFloat e toString
    var lucroSemZeros = parseFloat(lucroText).toString();

    // Atualizar o texto do elemento h1
    lucroElement.textContent = "Lucro: " + lucroSemZeros;
