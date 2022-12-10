import React, { useContext } from "react";

import Endpoint from "../Endpoint";
import Context from "../../Context";
import ProductTypesContainer from "./ProductTypesContainer";
import {
  transactionsCategories,
  authCategories,
  identityCategories,
  balanceCategories,
  investmentsCategories,
  investmentsTransactionsCategories,
  liabilitiesCategories,
  paymentCategories,
  assetsCategories,
  incomePaystubsCategories,
  transferCategories,
  transformAuthData,
  transformTransactionsData,
  transformBalanceData,
  transformInvestmentsData,
  transformInvestmentTransactionsData,
  transformLiabilitiesData,
  transformIdentityData,
  transformPaymentData,
  transformAssetsData,
  transformTransferData,
  transformIncomePaystubsData,
} from "../../dataUtilities";

const Products = () => {
  const { products } = useContext(Context);
  return (
    <h1></h1>
  );
};

Products.displayName = "Products";

export default Products;
