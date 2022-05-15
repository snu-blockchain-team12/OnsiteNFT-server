// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

// path allowance 문제 때문에 import 주소를 절대경로로 수정하였음(openzepplelin install필요 + 경로 수정 필요)

import "/Users/gunu/Documents/team12/nft/node_modules/openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";
import "/Users/gunu/Documents/team12/nft/node_modules/openzeppelin-solidity/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "/Users/gunu/Documents/team12/nft/node_modules/openzeppelin-solidity/contracts/access/Ownable.sol";
import "/Users/gunu/Documents/team12/nft/node_modules/openzeppelin-solidity/contracts/utils/Counters.sol";
import "/Users/gunu/Documents/team12/nft/node_modules/openzeppelin-solidity/contracts/token/ERC20/IERC20.sol";

// 찐막

contract NFT is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private deedId; // 디지털인증서의 고유번호 (단순 정수로 카운팅해서 발급) 

    constructor() ERC721("MyNFTs", "MNFT") {
        /**
        * "MyNFTs"라는 이름으로 Non-Fungible Token을 배포함
        * Token 심볼은 "MNFT"
        */
    }

    mapping(uint => string)  tokenURIs; // key(uint): deedId, value(string): pinata로 배포한 CID값 

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) 
    { 
        /**
        * 입력인자: deedId(tokenId) 
        * 반환값: tokenURI
        */
        return tokenURIs[tokenId];
    }

    function mintNFT(address to, string memory tokenURI) public returns (uint256)
    {
        /**
        * to: NFT소유권자 
        * to(주소)별 newDeedId(고유번호)가 발행이 되고, 고유번호를 조회하면 tokenURI가 호출되는 방식
        */
        deedId.increment(); // deedId는 increment를 호출할 때마다 1씩 증가함
        uint256 newDeedId = deedId.current();
        _mint(to, newDeedId); // 부모클래스의 mint 함수 호출
        tokenURIs[newDeedId] = tokenURI;

        return newDeedId;
    }

}