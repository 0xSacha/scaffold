import pytest
import asyncio

@pytest.mark.asyncio
async def test_contract(ctx_factory):
    ctx = ctx_factory()

    name1 = await ctx.contract.name().call()

    assert name1.result.name == 0

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'initialize',
        [111516399724901,2]
    )

    name2 = await ctx.contract.name().call()

    assert name2.result.name == 111516399724901

    symbol = await ctx.contract.symbol().call()

    assert symbol.result.symbol == 2



    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        '_setName',
        [555555]
    )

    name3 = await ctx.contract.name().call()

    assert name3.result.name == 555555

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        '_setSymbol',
        [555]
    )

    symbol2 = await ctx.contract.symbol().call()

    assert symbol2.result.symbol == 555

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'mint',
        [855,1,0,1,5]
    )

    #CHECK SUPPLY

    supply = await ctx.contract.totalSupply().call()

    assert supply.result.totalSupply == (1,0)

    supplyshares = await ctx.contract.sharesTotalSupply().call()

    assert supplyshares.result.sharesTotalSupply == (1,0)

    #CHECK INDEX

    tokenId = await ctx.contract.tokenByIndex((0,0)).call()

    assert tokenId.result.tokenId == (0,0)

    tokenOfOwnerByIndex = await ctx.contract.tokenOfOwnerByIndex(855,(0,0)).call()

    assert tokenOfOwnerByIndex.result.tokenId == (0,0)

    #CHECK METADATA

    balanceOf = await ctx.contract.balanceOf(855).call()

    assert balanceOf.result.balance == (1,0)

    ownerOf = await ctx.contract.ownerOf((0,0)).call()

    assert ownerOf.result.owner == 855

    sharesBalance = await ctx.contract.sharesBalance((0,0)).call()

    assert sharesBalance.result.sharesBalance == (1,0)
    
    sharePricePurchased = await ctx.contract.sharePricePurchased((0,0)).call()

    assert sharePricePurchased.result.sharePricePurchased == (1,5)
    
    mintedBlock = await ctx.contract.mintedBlock((0,0)).call()

    print(mintedBlock.result.mintedBlock)
    


    #CHECK TRANSFER 

    _aliceAddress = await ctx.alice.get_address().call()

    aliceAddress = _aliceAddress.result.res

    print(aliceAddress)


    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'mint',
        [aliceAddress,3,0,1,7]
    )

    ownerOf2 = await ctx.contract.ownerOf((1,0)).call()

    assert ownerOf2.result.owner == aliceAddress



    _bobAddress = await ctx.bob.get_address().call()

    bobAddress = _bobAddress.result.res
    

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'transferFrom',
        [aliceAddress,bobAddress,1,0]
    )  

    ownerOf3 = await ctx.contract.ownerOf((1,0)).call()

    assert ownerOf3.result.owner == bobAddress


    #CHECK SUB SHARES

    currentBobShares = await ctx.contract.sharesBalance((1,0)).call()

    assert currentBobShares.result.sharesBalance == (3,0)

    supply2 = await ctx.contract.totalSupply().call()

    assert supply2.result.totalSupply == (2,0)

    supplyshares2 = await ctx.contract.sharesTotalSupply().call()

    assert supplyshares2.result.sharesTotalSupply == (4,0)


    await ctx.execute(
        "bob",
        ctx.contract.contract_address,
        'subShares',
        [1,0,2,0]
    ) 

    newBobShares = await ctx.contract.sharesBalance((1,0)).call()

    assert newBobShares.result.sharesBalance == (1,0)

    supplyshares3 = await ctx.contract.sharesTotalSupply().call()

    assert supplyshares3.result.sharesTotalSupply == (2,0)

    #CHECK BURN 

    await ctx.execute(
        "bob",
        ctx.contract.contract_address,
        'burn',
        [1,0]
    ) 

    #ownerOf4 = await ctx.contract.ownerOf((1,0)).call()  validated

    supplyshares4 = await ctx.contract.sharesTotalSupply().call()

    assert supplyshares4.result.sharesTotalSupply == (1,0)

    supply3 = await ctx.contract.totalSupply().call()

    assert supply3.result.totalSupply == (1,0)

    balanceOf2 = await ctx.contract.balanceOf(bobAddress).call()

    assert balanceOf2.result.balance == (0,0)


    #APPROVE

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'mint',
        [aliceAddress,5,0,1,7]
    )

    ownerOf5 = await ctx.contract.ownerOf((1,0)).call()

    assert ownerOf5.result.owner == aliceAddress

    await ctx.execute(
        "alice",
        ctx.contract.contract_address,
        'approve',
        [bobAddress,1,0]
    )

    isApproved = await ctx.contract.getApproved((1,0)).call()

    assert isApproved.result.approved == bobAddress
    
    await ctx.execute(
        "bob",
        ctx.contract.contract_address,
        'transferFrom',
        [aliceAddress,bobAddress,1,0]
    )


    


