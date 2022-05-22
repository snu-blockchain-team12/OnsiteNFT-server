window.onload  = function() {
    if(window.ethereum !=="undefined") {
        this.ethereum.on("accountsChanged", handleAccountsChanged)
        
        window.ethereum.request({method: "eth_accounts"})
            .then(handleAccountsChanged)
            .catch((err)=>{
                console.log(err)
            })
    }
}

let accounts;

const handleAccountsChanged = (a) => {
    console.log("accounts changed")
    accounts = a
}

async function connectWallet() {
    accounts = await window.ethereum.request({method: "eth_requestAccounts"}).catch
        // 계정 없으면 오류를 리턴
        console.log(err.code)
    console.log(accounts)
}

async function checkBalance() {
    let balance = await window.ethereum.request( {method: "eth_getBalance",
        params: [
            accounts[0],
            'latest'
        ]
}).catch((err)=>{
    console.log(err)
})
    console.log(parseInt(balance)/Math.pow(10,18))
}

/// 프론트나 다른 Transaction에서 params를 받아서 사용해야함
async function sendTransaction(a) {
/*
paramas syntax
         params = [{
        "from": ,
        "to": ,
        "gas": ,
        "gaspPrice":,
        "value":,
        "data":,
    }]

*/
    await window.ethereum.request( {method: "eth_sendTransaction", a})
}

