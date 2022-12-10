import React, { useContext } from "react";
import Callout from "plaid-threads/Callout";
import Button from "plaid-threads/Button";
import InlineLink from "plaid-threads/InlineLink";

import Link from "../Link";
import Context from "../../Context";

import styles from "./index.module.scss";

const Header = () => {
  const {
    itemId,
    accessToken,
    linkToken,
    linkSuccess,
    isItemAccess,
    backend,
    linkTokenError,
    isPaymentInitiation,
  } = useContext(Context);

  return (
    <div className={styles.grid}>
      <h3 className={styles.title}>Plaid Link An account</h3>

      {!linkSuccess ? (
        <>
          <h4 className={styles.subtitle}>
            A sample end-to-end integration with Plaid
          </h4>
          <p className={styles.introPar}>
            The Plaid flow begins when your user wants to connect their bank
            account to your app. Simulate this by clicking the button below to
            launch Link - the client-side component that your users will
            interact with in order to link their accounts to Plaid and allow you
            to access their accounts via the Plaid API.
          </p>
          {/* message if backend is not running and there is no link token */}
          {!backend ? (
            <Callout warning>
              Unable to fetch link_token: please make sure your backend server
              is running and that your .env file has been configured with your
              <code>PLAID_CLIENT_ID</code> and <code>PLAID_SECRET</code>.
            </Callout>
          ) : /* message if backend is running and there is no link token */
          linkToken == null && backend ? (
            <Callout warning>
              <div>
                Unable to fetch link_token: please make sure your backend server
                is running and that your .env file has been configured
                correctly.
              </div>
              <div>
                If you are on a Windows machine, please ensure that you have
                cloned the repo with{" "}
                <InlineLink
                  href="https://github.com/plaid/quickstart#special-instructions-for-windows"
                  target="_blank"
                >
                  symlinks turned on.
                </InlineLink>{" "}
                You can also try checking your{" "}
                <InlineLink
                  href="https://dashboard.plaid.com/activity/logs"
                  target="_blank"
                >
                  activity log
                </InlineLink>{" "}
                on your Plaid dashboard.
              </div>
              <div>
                Error Code: <code>{linkTokenError.error_code}</code>
              </div>
              <div>
                Error Type: <code>{linkTokenError.error_type}</code>{" "}
              </div>
              <div>Error Message: {linkTokenError.error_message}</div>
            </Callout>
          ) : linkToken === "" ? (
            <div className={styles.linkButton}>
              <Button large disabled>
                Loading...
              </Button>
            </div>
          ) : (
            <div className={styles.linkButton}>
              <Link />
            </div>
          )}
        </>
      ) : (
        <>
          {isPaymentInitiation ? (
            <>
            <h4 className={styles.subtitle}>

              <p/>
              <Callout>
                You can see information of all your payments in the{' '}
                <InlineLink
                    href="https://dashboard.plaid.com/activity/payments"
                    target="_blank"
                >
                  Payments Dashboard
                </InlineLink>
                .
              </Callout>
            </h4>
            <p className={styles.requests}>

            </p>
          </>
          ) : /* If not using the payment_initiation product, show the item_id and access_token information */ (
            <>
            {isItemAccess ? (
                <h4 className={styles.subtitle}>

                </h4>
            ) : (
                <h4 className={styles.subtitle}>
                  <Callout warning>

                  </Callout>
                </h4>
            )}
            <div className={styles.itemAccessContainer}>
              <a href="http://127.0.0.1:8000/token" target="_blank">
          <div className={styles.linkButton}>
            <h5>Account has been authorized. </h5>
              <Button >
               Back to Home
              </Button>
            </div>
        </a>
            </div>
            {isItemAccess && (
                <p className={styles.requests}>

                </p>
            )}
          </>
          )}
        </>
      )}
    </div>
  );
};

Header.displayName = "Header";

export default Header;
